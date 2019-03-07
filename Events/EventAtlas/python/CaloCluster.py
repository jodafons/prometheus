
__all__ = ["CaloCluster"]


from EventCommon import EDM
from Gaugi  import StatusCode
from Gaugi  import Dataframe as DataframeEnum


class CaloCluster(EDM):
  # define all skimmed branches here.
  __eventBranches = {
      "SkimmedNtuple" : {'CaloCluster':[ # default skimmed ntuple branches
                         'el_e',
                         'el_calo_eta',
                         'el_calo_pt',
                         'el_etas2',
                          ],
                        'HLT__CaloCluster':[
                         'trig_EF_el_e',
                         'trig_EF_calo_eta',
                         'trig_EF_calo_pt',
                         'trig_EF_el_etas2',
                        ]},
      "PhysVal"       : {'CaloCluster':[
                          'el_calo_et',
                          'el_calo_eta',
                          'el_calo_phi',
                          'el_calo_etaBE2',
                          'el_calo_e',
                        ],
                         'HLT__CaloCluster':[
                          'trig_EF_el_calo_e',
                          'trig_EF_el_calo_et',
                          'trig_EF_el_calo_eta',
                          'trig_EF_el_calo_phi',
                          'trig_EF_el_calo_etaBE2',
                          'trig_EF_calo_loose',
                          'trig_EF_calo_medium',
                          'trig_EF_calo_tight',
                          'trig_EF_calo_lhvloose',
                          'trig_EF_calo_lhloose',
                          'trig_EF_calo_lhmedium',
                          'trig_EF_calo_lhtight', 
                          ] 
                          }
                }


  def __init__(self):
    EDM.__init__(self)
  

  def initialize(self):
    
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      if self._is_hlt:
        branches = self.__eventBranches['SkimmedNtuple']['HLT__CaloCluster']
      else:
        branches = self.__eventBranches['SkimmedNtuple']['CaloCluster']
      # Link all branches 
      for branch in branches:
        self._logger.debug(branch)
        self.setBranchAddress( self._tree, ('elCand%d_%s')%(self._elCand, branch)  , self._event)
        self._branches.append(branch) # hold all branches from the body class
    
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      if self._is_hlt:
        branches = self.__eventBranches["PhysVal"]["HLT__CaloCluster"]
      else:
        branches = self.__eventBranches["PhysVal"]["CaloCluster"]
      # loop over branches  
      for branch in branches:
        self.setBranchAddress( self._tree, branch  , self._event)
        self._branches.append(branch) # hold all branches from the body class
    else:
      self._logger.warning( "CaloCluster object can''t retrieved" )
      return StatusCode.FAILURE
    # Success

    return StatusCode.SUCCESS

  def et(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return getattr(self._event, 'elCand%d_el_et'%self._elCand)
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      if self._is_hlt:
        return self._event.trig_EF_el_calo_et[self.getPos()]
      else:
        return self._event.el_calo_et
    else:
      self._logger.warning("Impossible to retrieve the value of Calo Et.")
      return -999


  def eta(self):
    """
      Retrieve the Eta information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      if self._is_hlt:
        return getattr(self._event, 'elCand%d_trig_EF_calo_eta'%self._elCand)
      else:
        return getattr(self._event, 'elCand%d_el_calo_eta'%self._elCand)
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      if self._is_hlt:
        return self._event.trig_EF_el_calo_eta[self.getPos()]
      else:
        return self._event.el_calo_eta
    else:
      self._logger.warning("Impossible to retrieve the value of Calo Eta. Unknow dataframe.")
      return -999


  def phi(self):
    """
      Retrieve the Phi information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return -999
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      if self._is_hlt:
        return self._event.trig_EF_el_calo_phi[self.getPos()]
      else:
        return self._event.el_calo_phi
    else:
      self._logger.warning("Impossible to retrieve the value of Calo Phi. Unknow dataframe.")
      return -999

  def etaBE2(self):
    """
      Retrieve the EtaBE2 information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      if self._is_hlt:
        return getattr(self._event, 'elCand%d_trig_EF_el_etas2'%self._elCand)
      else:  
        return getattr(self._event, 'elCand%d_el_etas2'%self._elCand)
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      if self._is_hlt:
        return self._event.trig_EF_el_calo_etaBE2[self.getPos()]
      else:
        return self._event.el_calo_etaBE2
    else:
      self._logger.warning("Impossible to retrieve the value of Calo EtaBE2. Unknow dataframe.")
      return -999

  def energy(self):
    """
      Retrieve the E information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      if self._is_hlt:
        return getattr(self._event, 'elCand%d_trig_EF_el_e'%self._elCand)
      else:
        return getattr(self._event, 'elCand%d_el_e'%self._elCand)

    elif self._dataframe is DataframeEnum.PhysVal_v2:
      if self._is_hlt:
        return self._event.trig_EF_el_calo_e[self.getPos()]
      else:
        return self._event.el_calo_e
    else:
      self._logger.warning("Impossible to retrieve the value of Calo Energy. Unknow dataframe.")
      return -999


  def emCluster(self):
    """
      Retrieve the TrigEmCluster (FastCalo) python object into the Store Event
      For now, this is only available into the PhysVal dataframe.
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return self.getContext().getHandler('HLT__FastCalo')
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      cluster = self.getContext().getHandler('HLT__FastCalo')
      cluster.setPos(self.getPos())
      return cluster
    else:
      self._logger.warning("Impossible to retrieve the FastCalo object. Unknow dataframe")
      return None


      
  def size(self):
    """		
    	Retrieve the TrackParticle container size
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
    	return 1
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      if self._is_hlt:
        return self.event.trig_EF_el_calo_eta.size()
      else:
        return 1
    else:
      self._logger.warning("Impossible to retrieve the TrackParticle container size. Unknow dataframe")
 
  def empty(self):
    return False if self.size()>0 else True




