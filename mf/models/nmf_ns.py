
from nmf import *

class Nmf_ns(Nmf):
    """
    Implementation of the alternative model to manage factorizations that follow NMF model. This modification is 
    required by the Nonsmooth NMF algorithm (NSNMF) [14]. The Nonsmooth NMF algorithm is a modification of the standard divergence
    based NMF methods. By introducing a smoothing matrix it is aimed to achieve global sparseness. 
     
    It is the underlying model of matrix factorization and provides structure of modified standard NMF model. 
    
    .. attribute:: W
        
        Basis matrix -- the first matrix factor in the nonsmooth NMF model
        
    .. attribute:: H
    
        Mixture matrix -- the third matrix factor in the nonsmooth NMF model
        
    .. attribute:: S
    
        Smoothing matrix -- the middle matrix factor (V = WSH) in the nonsmooth NMF model
        
    The interpretation of the basis and mixture matrix is such as in the standard NMF model. The smoothing matrix is an
    extra square matrix whose entries depends on smoothing parameter theta which can be specified as algorithm specific model 
    option. For detailed explanation of the NSNMF algorithm see :mod:`methods.mf.nsnmf`.
        
    [14] Pascual-Montano, A., Carazo, J. M., Kochi, K., Lehmann, D., and Pascual-Marqui, R. D., (2006). Nonsmooth nonnegative matrix 
        factorization (nsnmf). IEEE transactions on pattern analysis and machine intelligence, 28(3), 403-415.
    """


    def __init__(self, params):
        """
        Construct factorization model that manages nonsmooth NMF models.
        
        :param params: MF runtime and algorithm parameters and options. For detailed explanation of the general model 
                       parameters see :mod:`mf`. For algorithm specific model options see documentation of chosen
                       factorization method. 
        :type params: `dict`
        """
        Nmf.__init__(self, params)
        if sp.isspmatrix(self.V) and (self.V.data < 0).any() or not sp.isspmatrix(self.V) and (self.V < 0).any():
            raise utils.MFError("The input matrix contains negative elements.") 
        
    def basis(self):
        """Return the matrix of basis vectors."""
        return self.W
    
    def coef(self):
        """Return the matrix of mixture coefficients."""
        return self.H
    
    def smoothing(self):
        """Return the smoothing matrix."""
        return self.S
    
    def fitted(self):
        """Compute the estimated target matrix according to the nonsmooth NMF algorithm model."""
        return dot(dot(self.W, self.S), self.H)
    
    def distance(self, metric = 'euclidean'):
        """Return the loss function value."""
        if metric == 'euclidean':
            return (sop(self.V - dot(dot(self.W, self.S), self.H), 2, pow)).sum()
        elif metric == 'kl': 
            Va = dot(dot(self.W, self.S), self.H)
            return (multiply(self.V, sop(elop(self.V, Va, div), op = log)) - self.V + Va).sum()
        else:
            raise utils.MFError("Unknown distance metric.")
    
    def residuals(self):
        """Return residuals between the target matrix and its nonsmooth NMF estimate."""
        return self.V - dot(dot(self.W, self.S), self.H)
        