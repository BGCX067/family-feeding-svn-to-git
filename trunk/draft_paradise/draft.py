# -*- coding: utf8 -*-

from lxml import etree
from copy import deepcopy
from itertools import product , izip
from pickle import dumps , loads
from operator import mul

def combinateDict ( params ) :
    keys = [ ]
    values = [ ]
    result = [ ]
    for key , value in params . items ( ) :
        keys . append ( key )
        values . append ( value )
    for comb in product ( * values ) :
        result . append ( dict ( izip ( keys , [ [ c ] for c in comb ] ) ) )
    if len ( result ) == 0 :
        result . append ( { } )
    return result

class MessagePattern :
    def __init__ ( self , name = str ( ) , args = { } ) :
        self . _name = str ( name )
        self . _args = dict ( args )
        self . _query = str ( )
        if len ( self . _name ) > 0 :
            self . _query += '[name/text()="%s"]' % self . _name
        for argName , argValue in self . _args . items ( ) :
            self . _query += '[args/%s/text()="%s"]' % ( argName , argValue )
    def find ( self , app ) :
        return app . getXPath ( '/world/runtime/messages/message' + self . _query )
    def match ( self , node ) :
        return len ( node . xpath ( 'self::*' + self . _query ) ) > 0
    def generate ( self , app ) :
        for messages in app . getXPath ( '/world/runtime/messages' ) :
            message =  '<message>\n'
            message += '    <name>%s</name>\n' % self . _name
            message += '    <args>\n'
            for arg , value in self . _args . items ( ) :
                message += '        <%s>%s</%s>\n' % ( arg , value , arg )
            message += '    </args>\n'
            message += '</message>\n'
            messages . append ( etree . fromstring ( message ) )

class SystemPattern :
    def __init__ ( self , name = str ( ) , uid = str ( ) , params = { } ) :
        self . _name = str ( name )
        self . _uid = str ( uid )
        self . _params = dict ( params )
        self . _query = str ( )
        if len ( self . _name ) > 0 :
            self . _query += '[name/text()="%s"]' % self . _name
        if len ( self . _uid ) > 0 :
            self . _query += '[uid/text()="%s"]' % self . _uid
        for param , values in self . _params . items ( ) :
            self . _query += '['
            self . _query += ' or ' . join ( [ 'params/%s/text()="%s"' % ( param , v ) for v in values ] )
            self . _query += ']'
    def changeUid ( self , uid ) :
        return SystemPattern ( self . _name , uid , self . _params )
    def combinate ( self ) :
        return [ SystemPattern ( name = self . _name , uid = self . _uid , params = p ) for p in combinateDict ( self . _params ) ]
    def find ( self , app ) :
        return app . getXPath ( '/world/runtime/systems/system' + self . _query )
    def generate ( self , app ) :
        for node in app . getXPath ( '/world/config/system[name/text()="%s"]' % self . _name ) :
            system = ''
            system += '<system>\n'
            system += '    <name>%s</name>' % self . _name
            system += '    <uid>%s</uid>' % self . _uid
            system += '    <params>\n'
            for param in node . xpath ( 'params/child::*' ) :
                value = param . text if param . text != None else str ( )
                system += '        <%s>%s</%s>\n' % ( param . tag , value , param . tag )
            system += '    </params>\n'
            for fsm in node . xpath ( 'fsm' ) :
                fsmName = fsm . xpath ( 'name/text()' ) . pop ( )
                system += '    <fsm>\n'
                system += '        <name>%s</name>\n' % fsmName
                system += '        <state>initial</state>\n'
                system += '        <inputs/>\n'
                system += '    </fsm>\n'
            system += '</system>\n'
            systemNode = etree . fromstring ( system )
            for systems in app . getXPath ( '/world/runtime/systems' ) :
                systems . append ( systemNode )
            sys = System ( app , systemNode )
            for param , values in self . _params . items ( ) :
                for value in values :
                    sys . setParam ( param , value )
            app . getReplication ( ) . systemSpawned ( sys )

class Replication :
    def __init__ ( self , node ) :
        self . _node = node
    def reset ( self ) :
        for spawn in self . _node . xpath ( 'spawn/*' ) :
            spawn . getparent ( ) . remove ( spawn )
        for kill in self . _node . xpath ( 'kill/*' ) :
            kill . getparent ( ) . remove ( kill )
        for change in self . _node . xpath ( 'change/*' ) :
            change . getparent ( ) . remove ( change )
    def apply ( self , app ) :
        for spawn in self . getSpawnSystems ( ) :
            SystemPattern ( name = spawn [ 'name' ] , uid = spawn [ 'uid' ] ) . generate ( app )
        for kill in self . getKillSystems ( ) :
            for system in app . getSystems ( SystemPattern ( uid = kill ) ) :
                system . kill ( )
        for change in self . getChangeSystems ( ) :
            for system in app . getSystems ( SystemPattern ( uid = change [ 'uid' ] ) ) :
                for param , value in change [ 'params' ] . items ( ) :
                    system . setParam ( param , value )
                for fsmName , state in change [ 'fsms' ] . items ( ) :
                    for fsm in system . getFsms ( name = fsmName ) :
                        fsm . setState ( state )
    def getSpawnSystems ( self ) :
        result = [ ]
        for system in self . _node . xpath ( 'spawn/system' ) :
            spawn = { }
            spawn [ 'name' ] = system . xpath ( 'name/text()' ) . pop ( )
            spawn [ 'uid' ] = system . xpath ( 'uid/text()' ) . pop ( )
            result . append ( spawn )
        return result
    def getKillSystems ( self ) :
        result = [ ]
        for uid in self . _node . xpath ( 'kill/uid/text()' ) :
            result . append ( uid )
        return result
    def getChangeSystems ( self ) :
        result = [ ]
        for system in self . _node . xpath ( 'change/system' ) :
            change = { }
            change [ 'uid' ] = system . xpath ( 'uid/text()' ) . pop ( )
            change [ 'params' ] = self . _getChanges ( system , 'params' )
            change [ 'fsms' ] = self . _getChanges ( system , 'fsms' )
            result . append ( change )
        return result
    def systemSpawned ( self , system ) :
        for rep in self . _node . xpath ( 'spawn' ) :
            spawn = ''
            spawn += '<system>\n'
            spawn += '    <name>%s</name>\n' % system . getName ( )
            spawn += '    <uid>%s</uid>\n' % system . getUid ( )
            spawn += '</system>\n'
            rep . append ( etree . fromstring ( spawn ) )
    def systemKilled ( self , system ) :
        for rep in self . _node . xpath ( 'change/system[uid/text()="%s"]' % system . getUid ( ) ) :
            rep . getparent ( ) . remove ( rep )
        for rep in self . _node . xpath ( 'spawn/system[uid/text()="%s"]' % system . getUid ( ) ) :
            rep . getparent ( ) . remove ( rep )
            return
        for rep in self . _node . xpath ( 'kill' ) :
            rep . append ( etree . fromstring ( '<uid>%s</uid>' % system . getUid ( ) ) )
    def stateChanged ( self , system , name , value , oldValue ) :
        self . _somethingChanged ( 'fsms' , system , name , value , oldValue )
    def paramChanged ( self , system , name , value , oldValue ) :
        self . _somethingChanged ( 'params' , system , name , value , oldValue )
    def _somethingChanged ( self , what , system , name , value , oldValue ) :
        if value == oldValue :
            return
        if value == str ( ) :
            oldParams = self . _node . xpath ( 'change/system[uid/text()="%s"][not(%s/%s/old/text())]' % ( system . getUid ( ) , what , name ) )
        else :
            oldParams = self . _node . xpath ( 'change/system[uid/text()="%s"][%s/%s/old/text()="%s"]' % ( system . getUid ( ) , what , name , value ) )
        for oldParam in oldParams :
            for param in self . _node . xpath ( 'change/system[uid/text()="%s"]/%s/%s' % ( system . getUid ( ) , what , name ) ) :
                param . getparent ( ) . remove ( param )
            self . _purgeChangeSystemNode ( system . getUid ( ) )
            return
        self . _keepChangeSystemNode ( system . getUid ( ) )
        for node in self . _node . xpath ( 'change/system[uid/text()="%s"]/%s/%s/new' % ( system . getUid ( ) , what , name ) ) :
            node . text = value if value != str ( ) else None
            return
        for node in self . _node . xpath ( 'change/system[uid/text()="%s"]/%s' % ( system . getUid ( ) , what ) ) :
            node . append ( etree . fromstring ( '<%s><new>%s</new><old>%s</old></%s>\n' % ( name , value , oldValue , name ) ) )
            return
    def _getChanges ( self , system , what ) :
        result = { }
        for param in system . xpath ( '%s/child::*' % what ) :
            value = str ( )
            for text in param . xpath ( 'new/text()' ) :
                value = text
            result [ param . tag ] = value
        return result
    def _purgeChangeSystemNode ( self , uid ) :
        if len ( self . _node . xpath ( 'change/system[uid/text()="%s"]/*/child::*' % uid ) ) > 0 :
            return
        for s in self . _node . xpath ( 'change/system[uid/text()="%s"]' % uid ) :
            s . getparent ( ) . remove ( s )
    def _keepChangeSystemNode ( self , uid ) :
        if len ( self . _node . xpath ( 'change/system[uid/text()="%s"]' % uid ) ) > 0 :
            return
        for rep in self . _node . xpath ( 'change' ) :
            change = ''
            change += '<system>\n'
            change += '    <uid>%s</uid>\n' % uid
            change += '    <params/>\n'
            change += '    <fsms/>\n'
            change += '</system>\n'
            rep . append ( etree . fromstring ( change ) )

class System :
    def __init__ ( self , app , node ) :
        self . _app = app
        self . _node = node
    def getName ( self ) :
        for name in self . _node . xpath ( 'name/text()' ) :
            return name
    def getUid ( self ) :
        for uid in self . _node . xpath ( 'uid/text()' ) :
            return uid
    def getParams ( self ) :
        result = { }
        for param in self . _node . xpath ( 'params/child::*' ) :
            result [ param . tag ] = param . text if param . text != None else str ( )
        return result
    def setParam ( self , name , value ) :
        for param in self . _node . xpath ( 'params/%s' % name ) :
            oldValue = param . text if param . text != None else str ( )
            param . text = value if value != str ( ) else None
            self . _app . getReplication ( ) . paramChanged ( self , name , value , oldValue )
    def kill ( self ) :
        self . _node . getparent ( ) . remove ( self . _node )
        self . _app . getReplication ( ) . systemKilled ( self )
    def getFsms ( self , name = str ( ) ) :
        result = [ ]
        query = 'fsm'
        if len ( name ) > 0 :
            query += '[name/text()="%s"]' % name
        for fsm in self . _node . xpath ( query ) :
            result . append ( Fsm ( self . _app , self , fsm ) )
        return result
    def getVaryingValues ( self , node ) :
        values = [ ]
        for valueXPath in node . xpath ( 'xpath/text()' ) :
            values += self . _app . getXPath ( valueXPath )
        for valueParam in node . xpath ( 'param/text()' ) :
            values . append ( self . getParams ( ) [ valueParam ] )
        for valueArg in node . xpath ( 'arg/text()' ) :
            values . append ( self . _app . getMessages ( MessagePattern ( ) ) . pop ( ) . getArgs ( ) [ valueArg ] )
        return values

class Transition :
    def __init__ ( self , fsm , state ) :
        self . _fsm = fsm
        self . _state = state
    def changeState ( self ) :
        self . _fsm . setState ( self . _state )

class Fsm :
    def __init__ ( self , app , system , node ) :
        self . _app = app
        self . _system = system
        self . _node = node
    def getName ( self ) :
        for name in self . _node . xpath ( 'name/text()' ) :
            return name
    def getState ( self ) :
        for state in self . _node . xpath ( 'state/text()' ) :
            return state
    def transite ( self ) :
        statePrev = str ( )
        stateFinal = self . getState ( )
        actions = [ ]
        while statePrev != stateFinal :
            statePrev = stateFinal
            for transition in self . _stateConfig ( stateFinal ) . xpath ( 'transition' ) :
                if self . _inputsMatch ( transition ) :
                    stateFinal = transition . xpath ( 'to_state/text()' ) . pop ( )
                    for action in self . _stateConfig ( statePrev ) . xpath ( 'on_exit/child::*' ) :
                        actions . append ( self . _app . action ( self . _system , action ) )
                    for action in self . _stateConfig ( stateFinal ) . xpath ( 'on_entry/child::*' ) :
                        actions . append ( self . _app . action ( self . _system , action ) )
                    break
        return actions , Transition ( self , stateFinal )
    def inputActions ( self ) :
        actions = [ ]
        for onInput in self . _stateConfig ( self . getState ( ) ) . xpath ( 'on_input' ) :
            if self . _inputsMatch ( onInput ) :
                for action in onInput . xpath ( 'actions/child::*' ) :
                    actions . append ( self . _app . action ( self . _system , action ) )
        return actions
    def computeInputs ( self ) :
        return [ self . _app . input ( self . _system , n ) . compute ( ) for n in self . _fsmConfig ( ) . xpath ( 'state/child::*/inputs/child::*' ) ]
    def setInputs ( self , inputs ) :
        for node in self . _node . xpath ( 'inputs' ) :
            node . text = dumps ( inputs )
    def getInputs ( self ) :
        for inputs in self . _node . xpath ( 'inputs/text()' ) :
            return loads ( inputs )
    def updateInputs ( self ) :
        self . setInputs ( self . computeInputs ( ) )
    def inputsChanged ( self ) :
        return self . getInputs ( ) != self . computeInputs ( )
    def setState ( self , newState ) :
        for state in self . _node . xpath ( 'state' ) :
            oldState = state . text
            state . text = newState
            self . _app . getReplication ( ) . stateChanged ( self . _system , self . getName ( ) , newState , oldState )
    def _inputsMatch ( self , context ) :
        for inputs in context . xpath ( 'inputs' ) :
            if 1 == reduce ( mul , [ self . _app . input ( self . _system , i ) . compute ( ) for i in inputs . xpath ( 'child::*' ) ] , 1 ) :
                return True
        return len ( context . xpath ( 'inputs' ) ) == 0
    def _fsmConfig ( self ) :
        for fsm in self . _node . xpath ( '/world/config/system[name/text()="%s"]/fsm[name/text()="%s"]' % ( self . _system . getName ( ) , self . getName ( ) ) ) :
            return fsm
    def _stateConfig ( self , stateName ) :
        for state in self . _fsmConfig ( ) . xpath ( 'state[name/text()="%s"]' % ( stateName ) ) :
            return state

class Message :
    def __init__ ( self , node ) :
        self . _node = node
    def getNode ( self ) :
        return self . _node
    def getName ( self ) :
        for name in self . _node . xpath ( 'name/text()' ) :
            return name
    def getArgs ( self ) :
        args = { }
        for arg in self . _node . xpath ( 'args/*' ) :
            args [ arg . tag ] = arg . text
        return args
    def kill ( self ) :
        self . _node . getparent ( ) . remove ( self . _node )

class ActionSetParam :
    def __init__ ( self , app , system , node ) :
        self . _app = app
        self . _system = system
        self . _node = node
    def execute ( self ) :
        name = self . _node . xpath ( 'name/text()' ) . pop ( )
        value = self . _system . getVaryingValues ( self . _node . xpath ( 'value' ) . pop ( ) ) . pop ( )
        self . _system . setParam ( name , value )

class ActionSendMessage :
    def __init__ ( self , app , system , node ) :
        self . _app = app
        self . _system = system
        self . _node = node
    def execute ( self ) :
        name = self . _node . xpath ( 'name/text()' ) . pop ( )
        args = { }
        for arg in self . _node . xpath ( 'args/child::*' ) :
            args [ arg . tag ] = self . _system . getVaryingValues ( arg ) . pop ( )
        self . _app . sendMessage ( MessagePattern ( name = name , args = args ) )

class InputAreEqual :
    def __init__ ( self , app , system , node ) :
        self . _app = app
        self . _system = system
        self . _node = node
    def compute ( self ) :
        values = set ( self . _system . getVaryingValues ( self . _node ) )
        return len ( values ) == 1

class InputMessageReceived :
    def __init__ ( self , app , system , node ) :
        self . _app = app
        self . _system = system
        self . _node = node
    def compute ( self ) :
        name = self . _node . xpath ( 'name/text()' ) . pop ( )
        args = { }
        for arg in self . _node . xpath ( 'args/child::*' ) :
            args [ arg . tag ] = self . _system . getVaryingValues ( arg ) . pop ( )
        for message in self . _app . getMessages ( MessagePattern ( ) ) :
            return MessagePattern ( name , args ) . match ( message . getNode ( ) )
        return False

class Application :
    def __init__ ( self , config , uid ) :
        world = ''
        world += '<world>\n'
        world += '    <runtime>\n'
        world += '        <systems/>\n'
        world += '        <messages/>\n'
        world += '    </runtime>\n'
        world += '</world>\n'
        self . _world = etree . fromstring ( world )
        self . _world . append ( etree . fromstring ( config ) )
        self . _appendReplicationNode ( )
        self . _uid = uid
    def action ( self , system , node ) :
        if node . tag == 'set_param' :
            return ActionSetParam ( self , system , node )
        elif node . tag == 'send_message' :
            return ActionSendMessage ( self , system , node )
    def input ( self , system , node ) :
        if node . tag == 'are_equal' :
            return InputAreEqual ( self , system , node )
        elif node . tag == 'message_received' :
            return InputMessageReceived ( self , system , node )
    def spawnSystems ( self , pattern ) :
        for p in pattern . combinate ( ) :
            p . changeUid ( self . _uid . getUid ( ) ) . generate ( self )
    def keepUniqueSystems ( self , pattern ) :
        for p in pattern . combinate ( ) :
            systems = self . getSystems ( p )
            for system in systems [ 1 : ] :
                system . kill ( )
            if len ( systems ) == 0 :
                self . spawnSystems ( p )
    def sendMessage ( self , pattern ) :
        pattern . generate ( self )
    def getMessages ( self , pattern ) :
        return [ Message ( m ) for m in pattern . find ( self ) ]
    def getSystems ( self , pattern ) :
        return [ System ( self , s ) for s in pattern . find ( self ) ]
    def getXPath ( self , path ) :
        return self . _world . xpath ( path )
    def getReplication ( self ) :
        for rep in self . _world . xpath ( '/world/runtime/replicate' ) :
            return Replication ( rep )
    def runSystems ( self ) :
        while True :
            actions , transitions = self . _systemsRunProduct ( )
            for transition in transitions :
                transition . changeState ( )
            for action in actions :
                action . execute ( )
            if len ( transitions ) + len ( actions ) == 0 :
                break
    def _systemsRunProduct ( self ) :
        actions = [ ]
        transitions = [ ]
        for system in self . getSystems ( SystemPattern ( ) ) :
            for fsm in system . getFsms ( ) :
                if fsm . inputsChanged ( ) :
                    fsm . updateInputs ( )
                    transiteActions , transition = fsm . transite ( )
                    inputActions = fsm . inputActions ( )
                    actions += inputActions
                    actions += transiteActions
                    transitions += [ transition ]
        return actions , transitions
    def _appendReplicationNode ( self ) :
        for runtime in self . _world . xpath ( '/world/runtime' ) :
            node = ''
            node += '<replicate>\n'
            node += '    <spawn/>\n'
            node += '    <kill/>\n'
            node += '    <change/>\n'
            node += '</replicate>\n'
            runtime . append ( etree . fromstring ( node ) )
