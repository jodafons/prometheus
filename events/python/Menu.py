
__all__ = ["Menu"]


from Gaugi.messenger.macros import *
from Gaugi import EDM, StatusCode, EnumStringification, ToolSvc
from prometheus.enumerations  import Dataframe as DataframeEnum
from EventAtlas import DecisionCore, AcceptType, Accept


class Menu(EDM):
    
  def __init__(self):
    EDM.__init__(self)


  def initialize(self):

    if not ToolSvc.retrieve("Emulator"):
      MSG_FATAL( self, "The emulator tool is not in the ToolSvc" )

    return StatusCode.SUCCESS

  
  def execute(self):
    MSG_DEBUG( self, "Clear all decorations..." )
    self.clearDecorations()
    return StatusCode.SUCCESS


  def finalize(self):
    return StatusCode.SUCCESS


  def accept( self, key ):


    # is in cache?
    if key in self.decorations():
      # decision in cache
      return self.getDecor( key )

    # get the accept decision from the TDT metadata
    elif self._dataframe is DataframeEnum.PhysVal_v2 and key.startswith('TDT__'):
      #  TDT__HLT__e28_lhtight_nod0_ivarloose
      #  TDT__EFCalo__e28_lhtight_nod0_ivarloose
      tdt = self.getContext().getHandler("HLT__TDT")
      trigInfo = key.split('__')
      tdt.core(DecisionCore.TriggerDecisionTool) # athena core
      # TDT__AcceptType__trigItem
      passed = tdt.ancestorPassed( 'HLT_'+trigInfo[-1], AcceptType.fromstring(trigInfo[1]) )
      accept = Accept( key )
      accept.setCutResult( 'pass', passed )
      self.setDecor( key, accept )
      return accept
    # get the accept decision from the Emulation metadata
    elif self._dataframe is DataframeEnum.PhysVal_v2 and key.startswith('EMU__'):
      #  EMU__HLT__e28_lhtight_nod0_ivarloose
      tdt = self.getContext().getHandler("HLT__TDT")
      trigInfo = key.split('__')
      tdt.core(DecisionCore.TrigEgammaEmulationTool) # athena emulation e/g core
      # EMU__AcceptType__trigItem
      passed = tdt.ancestorPassed( 'HLT_'+trigInfo[-1], AcceptType.fromstring(trigInfo[1]) )
      accept = Accept( key )
      accept.setCutResult( 'pass', passed )
      self.setDecor( key, accept )
      return accept
    
    # This name is not in metadata and not in cache, let's access the emulation svc and run it!
    else:  
      emulator = ToolSvc.retrieve( "Emulator" )
      if emulator.isValid( key ):
        accept = emulator.accept( self.getContext(), key )
        self.setDecor( key, accept )
        return accept
      else:
        MSG_FATAL( self, "It's is not possble to interpreter the key: %s.", key )









