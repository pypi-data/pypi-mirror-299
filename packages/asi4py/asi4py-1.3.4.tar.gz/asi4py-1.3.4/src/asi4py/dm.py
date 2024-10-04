from ctypes import cdll, CDLL, RTLD_GLOBAL
from ctypes import POINTER, byref, c_int, c_int64, c_int32, c_bool, c_char_p, c_double, c_void_p, CFUNCTYPE, py_object, cast, byref, Structure
import ctypes

from scipy.linalg import block_diag
from ase.data import chemical_symbols
from ase.geometry import get_distances
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.gaussian_process.kernels import RBF
from sklearn.kernel_ridge import KernelRidge

def get_elems_ordered(atoms):
  '''
    List elements in the order of tiers.
    https://gitlab.com/ase/ase/-/commit/7b70eddd026154d636faf404cc2f8c7b08d89667
    https://mail.python.org/pipermail/python-dev/2017-December/151283.html
  '''
  return list(dict.fromkeys(atoms.symbols))

def build_dm_free_atoms(atoms, elem_dms):
  '''
    Build atoms density matrix from single-atomic matrices for each element
  '''
  return block_diag(*[elem_dms[s] for s in atoms.symbols]).T

def load_atomic_dm(path, elem, tier):
  elemZ = chemical_symbols.index(elem)
  return np.load(f'{path}/{elemZ}_{elem}_{tier}.npz')['dm']

def save_atomic_dm(dm, path, elem, tier):
  elemZ = chemical_symbols.index(elem)
  return np.savez_compressed(f'{path}/{elemZ}_{elem}_{tier}.npz', dm=dm)

def bool2int_selector(atoms_selector):
  atoms_selector = np.array(atoms_selector)
  if np.issubdtype(atoms_selector.dtype, bool):
    atoms_selector = np.where(atoms_selector)[0]
  assert np.issubdtype(atoms_selector.dtype, np.integer)
  return atoms_selector

class PredictDMByAtoms:
  def __init__(self):
    pass
  
  def register_DM_init(self, asi):
    self.asi = asi
    asi.register_DM_init(PredictFreeAtoms.dm_init_callback, self)

  def dm_init_callback(self, iK, iS, descr, data):
    self = cast(self, py_object).value
    assert iK==1, "only G-point is supported"
    assert iS==1, "only RHF is supported"
    if self.asi.mpi_comm.rank == 0:
      print("PredictFreeAtoms.dm_init_callback")
    n_basis = self.asi.n_basis
    m = self(self.asi.atoms) if self.asi.scalapack.is_root(descr) else None
    
    assert m is None or (m.shape == (n_basis, n_basis)), \
                     f"m.shape=={m.shape} != n_basis=={n_basis}"
    self.asi.scalapack.scatter_numpy(m, descr, data)

  def __call__(self, atoms):
    raise RuntimeError("Not implemented in base class")
    #return build_dm_free_atoms(atoms, self.elem_dms)

class PredictFreeAtoms(PredictDMByAtoms):
  def __init__(self, elem_dms=None, elem_dm_path=None, elem_tiers=None):
    super().__init__()
    assert (elem_dms is None) != (elem_dm_path is None and elem_tiers is None)
    if elem_dms is None:
      elem_dms = {elem:load_atomic_dm(elem_dm_path, elem, tier) for elem, tier in elem_tiers.items()}
    self.elem_dms = elem_dms

  def __call__(self, atoms):
    return build_dm_free_atoms(atoms, self.elem_dms)

class PredictConstAtoms(PredictDMByAtoms):
  def __init__(self, const_atoms, const_dm):
    super().__init__()
    self.const_atoms = const_atoms
    self.const_dm = const_dm

  def __call__(self, atoms):
    np.testing.assert_allclose(atoms.numbers, self.const_atoms.numbers)
    
    np.testing.assert_allclose(
      atoms.positions - atoms.get_center_of_mass(), 
      self.const_atoms.positions - self.const_atoms.get_center_of_mass(), 
      atol=1e-1, rtol=1e-1)
    
    return self.const_dm

def select_basis_indices(all_basis_atoms, atoms_indices):
  return np.where(np.any(all_basis_atoms[None,:] == atoms_indices[:, None], axis=0))[0]

class PredictFrankensteinDM(PredictDMByAtoms):
  def __init__(self, predictors_and_selectors):
    # unzip https://stackoverflow.com/a/12974504/3213940
    self.predictors, atoms_selectors = list(zip(*predictors_and_selectors))
    self.atoms_groups_indices = list(map(bool2int_selector, atoms_selectors))

    if True: # extended assertion check
      all_selected_atoms_set = set().union(*self.atoms_groups_indices)
      max_range_atoms_set = set(range(max(all_selected_atoms_set) + 1))
      missed_atoms = max_range_atoms_set - all_selected_atoms_set
      # Heuristic check: doesn't guarantie full atoms coverage, because actual
      # number of atoms is not known here and max(all_selected_atoms_set) is 
      # just an heuristic
      assert len(missed_atoms) == 0, f"Missed atoms: {missed_atoms}"
  
  def register_DM_init(self, asi):
    super().register_DM_init(asi)
    self.init_basis_indices(asi)

  def init_basis_indices(self, asi):
    all_basis_atoms = asi.basis_atoms
    self.basis_indices = [select_basis_indices(all_basis_atoms, atoms_group) for atoms_group in self.atoms_groups_indices]
    self.n_basis = asi.n_basis

    if True:
      all_selected_basis_indices = set().union(*self.basis_indices)
      total_basis_set = set(range(self.n_basis))
      missed_basis_functions = total_basis_set - all_selected_basis_indices
      assert len(missed_basis_functions) == 0, f'Basis functions missed from selection: {missed_basis_functions}'

  def __call__(self, atoms):
    assert len(self.predictors) == len(self.atoms_groups_indices)
    assert len(self.predictors) == len(self.basis_indices)

    total_dm = np.zeros((self.n_basis, self.n_basis), dtype=np.float64)
    total_dm_cnt = np.zeros(total_dm.shape, dtype=int)
    for predictor, atoms_group_indices, basis_group_indices in zip(self.predictors, self.atoms_groups_indices, self.basis_indices):
      total_dm[basis_group_indices[np.newaxis,:], basis_group_indices[:, np.newaxis]] += predictor(atoms[atoms_group_indices])
      total_dm_cnt[basis_group_indices[np.newaxis,:], basis_group_indices[:, np.newaxis]] += 1
    
    assert (total_dm[total_dm_cnt==0]==0).all()
    total_dm_cnt[total_dm_cnt==0] = 1 # to avoid division by zero

    return (total_dm / total_dm_cnt).T

class PredictSeqDM(PredictDMByAtoms):
  def __init__(self, base_predictor, n_hist):
    self.base_predictor = base_predictor
    self.preds = []
    self.descrs = []
    self.errs = []
    self.n_hist = n_hist
  
  def __call__(self, atoms):
    predicted_dm = self.base_predictor(atoms)

    #descr = np.array([])
    #descr = atoms.positions - np.mean(atoms.positions, axis=0)
    R,d = get_distances(atoms.positions)
    #invd = invd * atoms.numbers[:,np.newaxis] * atoms.numbers[np.newaxis, :]
    lowtri = np.tri(len(atoms), len(atoms), -1)==1
    #R = R[lowtri]
    invd = 1/d[lowtri]
    #R = R * invd[:, np.newaxis]
    #descr = np.vstack([R.T,invd]).ravel()
    descr = invd
    #descr = (atoms.positions[np.newaxis, :, :] - atoms.positions[:, np.newaxis,:])[np.where(np.tri(len(atoms), len(atoms), -1))]
    #descr = np.hstack([descr, self.S.ravel()])
    #descr = self.S[np.where(np.tri(self.S.shape[0], self.S.shape[1], -1)==1.0)]

    #lowtri = np.tri(*predicted_dm.shape, 0)==1
    #descr = predicted_dm[lowtri]
    
    predicted_err = self.predict_err(predicted_dm, descr)
    print ("predicted_err", np.linalg.norm(predicted_err) / ((len(atoms) // 3)**0.5) )
    if len(self.preds) == self.n_hist:
      self.preds.pop(0)
      self.descrs.pop(0)
      self.errs.pop(0)
    self.preds.append(predicted_dm)
    self.descrs.append(descr)

    return (predicted_dm - predicted_err).T
  
  def update_errs(self, exact_dm):
    assert len(self.preds) == len(self.errs) + 1
    self.errs.append(self.preds[-1] - exact_dm)
  
  def predict_err(self, predicted_dm, descr):

    k = len(self.preds)
    assert k == len(self.descrs)
    assert k == len(self.errs)
    if k == 0:
      return np.zeros(predicted_dm.shape)
    
    X = np.hstack([np.array(self.preds).reshape((k, -1)), np.array(self.descrs).reshape((k, -1))])
    x = np.hstack([predicted_dm.ravel(), descr.ravel()]).reshape((1, -1))
    Y = np.array(self.errs).reshape((k, -1))
    
    X_mean = np.mean(X, axis=0)
    Y_mean = np.mean(Y, axis=0)
    
    X -= X_mean
    Y -= Y_mean
    x -= X_mean
    #------------------
    

    reg = KernelRidge(alpha=1e-15, kernel='rbf')
    reg.fit(X, Y)
    y = reg.predict(x)

    #------------------
    y += Y_mean
    return y.reshape(predicted_dm.shape)
    



