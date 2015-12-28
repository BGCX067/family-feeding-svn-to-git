# -*- coding: utf8 -*-

# TODO:
# - Действие на создание системы
# - Действие на keep unique systems
# - Действие на удаление системы
# - Отправка/получение сообщений клиентом
# - Отправка/получение сообщений системой
# - Отработка очереди сообщений
# - Определение систем, подверженных изменению
# - Запрос репликации отсутствующих систем

import unittest
import draft
from lxml import etree

def getSystems ( app , ** kw_args ) :
    return app . getSystems ( draft . SystemPattern ( ** kw_args ) )

def getMessages ( app , ** kw_args ) :
    return app . getMessages ( draft . MessagePattern ( ** kw_args ) )

def sendMessage ( app , ** kw_args ) :
    app . sendMessage ( draft . MessagePattern ( ** kw_args ) )

def spawnSystems ( app , ** kw_args ) :
    app . spawnSystems ( draft . SystemPattern ( ** kw_args ) )

def keepUniqueSystems ( app , ** kw_args ) :
    app . keepUniqueSystems ( draft . SystemPattern ( ** kw_args ) )

class TestUidProvider :
    def __init__ ( self , uids ) :
        self . uids = uids
    def getUid ( self ) :
        return self . uids . pop ( )
                
class ApplicationTestCase ( unittest . TestCase ) :
    def setUp ( self ) :
        config = ''
        config += '<config>\n'
        config += '    <test>\n'
        config += '        <test1>test1</test1>\n'
        config += '        <test2>test2</test2>\n'
        config += '        <param1>\n'
        config += '            <value>test11</value>\n'
        config += '            <value>test12</value>\n'
        config += '        </param1>\n'
        config += '        <param2>\n'
        config += '            <value>test21</value>\n'
        config += '            <value>test22</value>\n'
        config += '        </param2>\n'
        config += '    </test>\n'
        config += '    <system>\n'
        config += '        <name>system1</name>\n'
        config += '        <params>\n'
        config += '            <param1>value1</param1>\n'
        config += '            <param2>value2</param2>\n'
        config += '            <param3/>\n'
        config += '        </params>\n'
        config += '    </system>\n'
        config += '    <system>\n'
        config += '        <name>system2</name>\n'
        config += '        <params>\n'
        config += '            <param1>value1</param1>\n'
        config += '            <param2>value22</param2>\n'
        config += '            <param3/>\n'
        config += '        </params>\n'
        config += '    </system>\n'
        config += '</config>\n'
        uids = [ 'uid1' , 'uid2' , 'uid3' , 'uid4' , 'uid5' ]
        uids . reverse ( )
        uidsProvider = TestUidProvider ( uids )
        self . app = draft . Application ( config = config , uid = uidsProvider )
    def testSpawnOneSystem ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        systems = getSystems ( self . app )
        self . assertEqual ( [ 'system1' ] , [ s . getName ( ) for s in systems ] )
        self . assertEqual ( [ 'uid1' ] , [ s . getUid ( ) for s in systems ] )
        self . assertEqual ( [ { 'param1' : 'value1' , 'param2' : 'value2' , 'param3' : '' } ] , [ s . getParams ( ) for s in systems ] )
    def testSpawnSameSystems ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        spawnSystems ( self . app , name = 'system1' )
        systems = getSystems ( self . app )
        self . assertEqual ( [ 'system1' , 'system1' ] , [ s . getName ( ) for s in systems ] )
    def testSpawnSystemParams ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'v1' ] } )
        systems = getSystems ( self . app )
        self . assertEqual ( [ { 'param1' : 'v1' , 'param2' : 'value2' , 'param3' : '' } ] , [ s . getParams ( ) for s in systems ] )
    def testSpawnSystemsXPath ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = \
            { 'param1' : self . app . getXPath ( '/world/config/test/param1/value/text()' )
            , 'param2' : self . app . getXPath ( '/world/config/test/param2/value/text()' )
            } )
        self . assertEqual ( 4 , len ( getSystems ( self . app ) ) )
        self . assertEqual ( 1 , len ( getSystems ( self . app , params = { 'param1' : [ 'test11' ] , 'param2' : [ 'test21' ] } ) ) )
        self . assertEqual ( 1 , len ( getSystems ( self . app , params = { 'param1' : [ 'test11' ] , 'param2' : [ 'test22' ] } ) ) )
        self . assertEqual ( 1 , len ( getSystems ( self . app , params = { 'param1' : [ 'test12' ] , 'param2' : [ 'test21' ] } ) ) )
        self . assertEqual ( 1 , len ( getSystems ( self . app , params = { 'param1' : [ 'test12' ] , 'param2' : [ 'test22' ] } ) ) )
    def testSpawnSystemsXPathParams ( self ) :
        spawnSystems \
            ( self . app
            , name = 'system1' 
            , params = { 'param3' : [ 'test3' ] , 'param1' : self . app . getXPath ( '/world/config/system[name/text()="system1"]/params/param1/text()' ) }
            )
        self . assertEqual ( 1 , len ( getSystems ( self . app , params = { 'param3' : [ 'test3' ] } ) ) )
    def testKeepUniqueSystemsByName ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] } )
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test2' ] } )
        keepUniqueSystems ( self . app , name = 'system1' )
        keepUniqueSystems ( self . app , name = 'system2' )
        self . assertEqual ( 1 , len ( getSystems ( self . app , name = 'system1' ) ) )
        self . assertEqual ( 1 , len ( getSystems ( self . app , name = 'system2' ) ) )
        self . assertEqual ( 1 , len ( getSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] } ) ) )
    def testKeepUniqueSystemsByParams ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test2' ] } )
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] , 'param3' : [ 'test31' ] } )
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] , 'param3' : [ 'test32' ] } )
        keepUniqueSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] } )
        keepUniqueSystems ( self . app , name = 'system2' , params = { 'param1' : [ 'test1' ] } )
        self . assertEqual ( 3 , len ( getSystems ( self . app ) ) )
        self . assertEqual ( 1 , len ( getSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] , 'param3' : [ 'test31' ] } ) ) )
        self . assertEqual ( 1 , len ( getSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test2' ] } ) ) )
        self . assertEqual ( 1 , len ( getSystems ( self . app , name = 'system2' , params = { 'param1' : [ 'test1' ] } ) ) )
    def testKeepUniqueSystemsXPath ( self ) :
        keepUniqueSystems \
            ( self . app
            , name = 'system1' 
            , params = { 'param1' : self . app . getXPath ( '/world/config/system[name/text()="system1"]/params/param1/text()' ) }
            )
        self . assertEqual ( 1 , len ( getSystems ( self . app ) ) )
    def testGetSystemsByName ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        spawnSystems ( self . app , name = 'system2' )
        systems = getSystems ( self . app , name = 'system1' )
        self . assertEqual ( [ 'system1' ] , [ s . getName ( ) for s in systems ] )
    def testGetSystemsByUid ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        spawnSystems ( self . app , name = 'system2' )
        systems = getSystems ( self . app , uid = 'uid1' )
        self . assertEqual ( [ 'system1' ] , [ s . getName ( ) for s in systems ] )
    def testGetSystemsByParams ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        spawnSystems ( self . app , name = 'system2' )
        systems = getSystems ( self . app , params = { 'param1' : [ 'value1' ] , 'param2' : [ 'value2' ] } )
        self . assertEqual ( [ 'system1' ] , [ s . getName ( ) for s in systems ] )
    def testGetSystemsByParamsXPath ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        spawnSystems ( self . app , name = 'system2' )
        systems = getSystems ( self . app , params = { 'param2' : self . app . getXPath ( '/world/config/system/params/param2/text()' ) } )
        self . assertEqual ( [ 'system1' , 'system2' ] , [ s . getName ( ) for s in systems ] )

class SystemTestCase ( unittest . TestCase ) :
    def setUp ( self ) :
        config = ''
        config += '<config>\n'
        config += '    <system>\n'
        config += '        <name>system1</name>\n'
        config += '        <params>\n'
        config += '            <param1>value1</param1>\n'
        config += '        </params>\n'
        config += '    </system>\n'
        config += '</config>\n'
        uids = [ 'uid1' ]
        uids . reverse ( )
        uidsProvider = TestUidProvider ( uids )
        self . app = draft . Application ( config = config , uid = uidsProvider )
    def testKillSystem ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        system = getSystems ( self . app ) . pop ( )
        system . kill ( )
        self . assertEqual ( 0 , len ( getSystems ( self . app ) ) )
    def testSetParam ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        system = getSystems ( self . app ) . pop ( )
        system . setParam ( 'param1' , 'value11' )
        self . assertEqual ( 1 , len ( getSystems ( self . app , params = { 'param1' : [ 'value11' ] } ) ) )
    def testSetParamUnknown ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        system = getSystems ( self . app ) . pop ( )
        system . setParam ( 'unknown' , 'value' )
        self . assertEqual ( 0 , len ( getSystems ( self . app , params = { 'unknown' : [ 'value' ] } ) ) )

class ReplicationTestCase ( unittest . TestCase ) :
    def setUp ( self ) :
        config = ''
        config += '<config>\n'
        config += '    <system>\n'
        config += '        <name>system1</name>\n'
        config += '        <params>\n'
        config += '            <param1>value1</param1>\n'
        config += '            <param2>value2</param2>\n'
        config += '            <param3/>\n'
        config += '        </params>\n'
        config += '        <fsm>\n'
        config += '            <name>fsm1</name>\n'
        config += '            <state> <name>state1</name> </state>\n'
        config += '            <state> <name>state2</name> </state>\n'
        config += '        </fsm>\n'
        config += '    </system>\n'
        config += '    <system>\n'
        config += '        <name>system2</name>\n'
        config += '    </system>\n'
        config += '</config>\n'
        uids = [ 'uid1' , 'uid2' , 'uid3' , 'uid4' , 'uid5' ]
        uids . reverse ( )
        uidsProvider = TestUidProvider ( uids )
        self . app = draft . Application ( config = config , uid = uidsProvider )
        self . app2 = draft . Application ( config = config , uid = uidsProvider )
    def testReplicationSpawnSystems ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        rep = self . app . getReplication ( )
        self . assertEqual ( [ { 'name' : 'system1' , 'uid' : 'uid1' } ] , rep . getSpawnSystems ( ) )
    def testResetReplication ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        self . app . getReplication ( ) . reset ( )
        spawnSystems ( self . app , name = 'system2' )
        rep = self . app . getReplication ( )
        self . assertEqual ( [ { 'name' : 'system2' , 'uid' : 'uid2' } ] , rep . getSpawnSystems ( ) )
    def testReplicationChangeParams ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] , 'param2' : [ 'test' ] } )
        system = getSystems ( self . app ) . pop ( )
        system . setParam ( 'param2' , 'test2' )
        rep = self . app . getReplication ( )
        self . assertEqual ( [ { 'uid' : 'uid1' , 'params' : { 'param1' : 'test1' , 'param2' : 'test2' } , 'fsms' : { } } ] , rep . getChangeSystems ( ) )
    def testReplicationChangeParamsNoChanges ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] } )
        self . app . getReplication ( ) . reset ( )
        system = getSystems ( self . app ) . pop ( )
        system . setParam ( 'param1' , 'test11' )
        system . setParam ( 'param1' , 'test1' )
        system . setParam ( 'param2' , 'value2' )
        rep = self . app . getReplication ( )
        self . assertEqual ( 0 , len ( rep . getChangeSystems ( ) ) )
    def testReplicationChangeParamsEmptyValue ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ '' ] } )
        rep = self . app . getReplication ( )
        self . assertEqual ( [ { 'uid' : 'uid1' , 'params' : { 'param1' : '' } , 'fsms' : { } } ] , rep . getChangeSystems ( ) )
    def testReplicationChangeParamsEmptyValueNoChanges ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ '' ] } )
        self . app . getReplication ( ) . reset ( )
        system = getSystems ( self . app ) . pop ( )
        system . setParam ( 'param1' , 'test' )
        system . setParam ( 'param1' , '' )
        rep = self . app . getReplication ( )
        self . assertEqual ( [ ] , rep . getChangeSystems ( ) )
    def testReplicationChangeParamsDefault ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] , 'param2' : [ 'test2' ] } )
        system = getSystems ( self . app ) . pop ( )
        system . setParam ( 'param2' , 'value2' )
        rep = self . app . getReplication ( )
        self . assertEqual ( [ { 'uid' : 'uid1' , 'params' : { 'param1' : 'test1' } , 'fsms' : { } } ] , rep . getChangeSystems ( ) )
    def testReplicationChangeParamsDefaultNoChanges ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] } )
        system = getSystems ( self . app ) . pop ( )
        system . setParam ( 'param1' , 'value1' )
        rep = self . app . getReplication ( )
        self . assertEqual ( 0 , len ( rep . getChangeSystems ( ) ) )
    def testReplicationChangeState ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        system = getSystems ( self . app ) . pop ( )
        fsm = system . getFsms ( ) . pop ( )
        fsm . setState ( 'state1' )
        rep = self . app . getReplication ( )
        self . assertEqual ( [ { 'uid' : 'uid1' , 'fsms' : { 'fsm1' : 'state1' } , 'params' : { } } ] , rep . getChangeSystems ( ) )
    def testReplicationKillSystems ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        self . app . getReplication ( ) . reset ( )
        system = getSystems ( self . app ) . pop ( )
        system . kill ( )
        rep = self . app . getReplication ( )
        self . assertEqual ( [ 'uid1' ] , rep . getKillSystems ( ) )
    def testReplicationKillSystemsRedundant ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        system = getSystems ( self . app ) . pop ( )
        system . setParam ( 'param1' , 'test1' )
        system . kill ( )
        rep = self . app . getReplication ( )
        self . assertEqual ( 0 , len ( rep . getKillSystems ( ) ) )
        self . assertEqual ( 0 , len ( rep . getSpawnSystems ( ) ) )
        self . assertEqual ( 0 , len ( rep . getChangeSystems ( ) ) )
    def testApplyReplicationSpawn ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        self . app . getReplication ( ) . apply ( self . app2 )
        system = getSystems ( self . app2 , name = 'system1' ) . pop ( )
        self . assertEqual ( 'uid1' , system . getUid ( ) )
    def testApplyReplicationKill ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        self . app . getReplication ( ) . apply ( self . app2 )
        self . app . getReplication ( ) . reset ( )
        system = getSystems ( self . app , name = 'system1' ) . pop ( )
        system . kill ( )
        self . app . getReplication ( ) . apply ( self . app2 )
        self . assertEqual ( 0 , len ( getSystems ( self . app2 ) ) )
    def testApplyReplicationChange ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] } )
        getSystems ( self . app ) . pop ( ) . getFsms ( ) . pop ( ) . setState ( 'state1' )
        self . app . getReplication ( ) . apply ( self . app2 )
        system = getSystems ( self . app2 , name = 'system1' ) . pop ( )
        fsm = system . getFsms ( ) . pop ( )
        self . assertEqual ( { 'param1' : 'test1' , 'param2' : 'value2' , 'param3' : '' } , system . getParams ( ) )
        self . assertEqual ( 'state1' , fsm . getState ( ) )

class ActionsTestCase ( unittest . TestCase ) :
    def setUp ( self ) :
        config = ''
        config += '<config>\n'
        config += '    <test>\n'
        config += '        <test1>test1</test1>\n'
        config += '    </test>\n'
        config += '    <system>\n'
        config += '        <name>system1</name>\n'
        config += '        <params>\n'
        config += '            <param1>value1</param1>\n'
        config += '            <param2>value2</param2>\n'
        config += '            <param3>value3</param3>\n'
        config += '            <param4>value4</param4>\n'
        config += '        </params>\n'
        config += '    </system>\n'
        config += '</config>\n'
        uids = [ 'uid1' ]
        uids . reverse ( )
        uidsProvider = TestUidProvider ( uids )
        self . app = draft . Application ( config = config , uid = uidsProvider )
    def actionExecute ( self , system , text ) :
        self . app . action ( system , etree . fromstring ( text ) ) . execute ( )
    def testActionSetParam ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param3' : [ 'test3' ] } )
        system = getSystems ( self . app ) . pop ( )
        sendMessage ( self . app , name = 'message1' , args = { 'arg1' : 'test4' } )
        self . actionExecute ( system , '<set_param> <name>param1</name> <value><xpath>/world/config/test/test1/text()</xpath></value> </set_param>' )
        self . actionExecute ( system , '<set_param> <name>param2</name> <value><param>param3</param></value> </set_param>' )
        self . actionExecute ( system , '<set_param> <name>param4</name> <value><arg>arg1</arg></value> </set_param>' )
        self . assertEqual ( 1 , len ( getSystems ( self . app , params = { 'param1' : [ 'test1' ] , 'param2' : [ 'test3' ] , 'param4' : [ 'test4' ] } ) ) )
    def testActionSendMessage ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param2' : [ 'test2' ] } )
        system = getSystems ( self . app ) . pop ( )
        self . actionExecute ( system , '<send_message> <name>message1</name> </send_message>' )
        self . actionExecute ( system , '<send_message> <name>message2</name> <args><arg1><xpath>/world/config/test/test1/text()</xpath></arg1></args> </send_message>' )
        self . actionExecute ( system , '<send_message> <name>message3</name> <args><arg2><param>param2</param></arg2></args> </send_message>' )
        self . assertEqual ( 1 , len ( getMessages ( self . app , name = 'message1' ) ) )
        self . assertEqual ( 1 , len ( getMessages ( self . app , name = 'message2' , args = { 'arg1' : 'test1' } ) ) )
        self . assertEqual ( 1 , len ( getMessages ( self . app , name = 'message3' , args = { 'arg2' : 'test2' } ) ) )

class InputsTestCase ( unittest . TestCase ) :
    def setUp ( self ) :
        config = ''
        config += '<config>\n'
        config += '    <test>\n'
        config += '        <test1>test1</test1>\n'
        config += '    </test>\n'
        config += '    <system>\n'
        config += '        <name>system1</name>\n'
        config += '        <params>\n'
        config += '            <param1>value1</param1>\n'
        config += '            <param2>value2</param2>\n'
        config += '        </params>\n'
        config += '    </system>\n'
        config += '</config>\n'
        uids = [ 'uid1' ]
        uids . reverse ( )
        uidsProvider = TestUidProvider ( uids )
        self . app = draft . Application ( config = config , uid = uidsProvider )
    def inputCompute ( self , system , text ) :
        return self . app . input ( system , etree . fromstring ( text ) ) . compute ( )
    def testInputAreEqual ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] , 'param2' : [ 'test2' ] } )
        system = getSystems ( self . app ) . pop ( )
        self . assertEqual ( True  , self . inputCompute ( system , '<are_equal> <param>param1</param> <xpath>/world/config/test/test1/text()</xpath> </are_equal>' ) )
        self . assertEqual ( False , self . inputCompute ( system , '<are_equal> <param>param2</param> <xpath>/world/config/test/test1/text()</xpath> </are_equal>' ) )
    def testInputMessageReceived ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] } )
        system = getSystems ( self . app ) . pop ( )
        self . assertEqual ( False , self . inputCompute ( system , '<message_received> <name>message1</name> </message_received>' ) )
        sendMessage ( self . app , name = 'message1' , args = { 'arg1' : 'test1' } )
        self . assertEqual ( True  , self . inputCompute ( system , '<message_received> <name>message1</name> </message_received>' ) )
        self . assertEqual ( True  , self . inputCompute ( system , '<message_received> <name>message1</name> <args><arg1><param>param1</param></arg1></args> </message_received>' ) )
        self . assertEqual ( False , self . inputCompute ( system , '<message_received> <name>message1</name> <args><arg2><param>param1</param></arg2></args> </message_received>' ) )
        self . assertEqual ( False , self . inputCompute ( system , '<message_received> <name>message2</name> </message_received>' ) )

class MessagingTestCase ( unittest . TestCase ) :
    def setUp ( self ) :
        config = ''
        config += '<config>\n'
        config += '    <system>\n'
        config += '        <name>system1</name>\n'
        config += '        <params>\n'
        config += '            <param1>value1</param1>\n'
        config += '            <param2>value2</param2>\n'
        config += '        </params>\n'
        config += '    </system>\n'
        config += '</config>\n'
        uids = [ ]
        uids . reverse ( )
        uidsProvider = TestUidProvider ( uids )
        self . app = draft . Application ( config = config , uid = uidsProvider )
    def testGetMessages ( self ) :
        sendMessage ( self . app , name = 'message1' )
        sendMessage ( self . app , name = 'message2' )
        self . assertEqual ( 2 , len ( getMessages ( self . app ) ) )
    def testGetMessagesByName ( self ) :
        sendMessage ( self . app , name = 'message1' )
        self . assertEqual ( 1 , len ( getMessages ( self . app , name = 'message1' ) ) )
        self . assertEqual ( 0 , len ( getMessages ( self . app , name = 'message2' ) ) )
    def testGetMessagesByArgs ( self ) :
        sendMessage ( self . app , name = 'message1' , args = { 'arg1' : 'test1' } )
        self . assertEqual ( 1 , len ( getMessages ( self . app , args = { 'arg1' : 'test1' } ) ) )
        self . assertEqual ( 0 , len ( getMessages ( self . app , args = { 'arg3' : 'test3' } ) ) )
    def testMessageGetArgs ( self ) :
        sendMessage ( self . app , name = 'message1' , args = { 'arg1' : 'test1' } )
        message = getMessages ( self . app ) . pop ( )
        self . assertEqual ( { 'arg1' : 'test1' } , message . getArgs ( ) )
    def testClearMessages ( self ) :
        sendMessage ( self . app , name = 'message1' )
        msg = getMessages ( self . app ) . pop ( )
        msg . kill ( )
        self . assertEqual ( 0 , len ( getMessages ( self . app ) ) )

class FsmTestCase ( unittest . TestCase ) :
    def setUp ( self ) :
        config = ''
        config += '<config>\n'
        config += '    <system>\n'
        config += '        <name>system1</name>\n'
        config += '        <fsm>\n'
        config += '            <name>fsm1</name>\n'
        config += '            <state> <name>state1</name> </state>\n'
        config += '            <state> <name>state2</name> </state>\n'
        config += '        </fsm>\n'
        config += '        <fsm>\n'
        config += '            <name>fsm2</name>\n'
        config += '            <state> <name>state1</name> </state>\n'
        config += '            <state> <name>state2</name> </state>\n'
        config += '        </fsm>\n'
        config += '    </system>\n'
        config += '</config>\n'
        uids = [ 'uid1' ]
        uids . reverse ( )
        uidsProvider = TestUidProvider ( uids )
        self . app = draft . Application ( config = config , uid = uidsProvider )
    def testGetFsms ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        system = getSystems ( self . app ) . pop ( )
        self . assertEqual ( [ 'fsm1' ] , [ f . getName ( ) for f in system . getFsms ( name = 'fsm1' ) ] )
    def testGetName ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        system = getSystems ( self . app ) . pop ( )
        self . assertEqual ( [ 'fsm1' , 'fsm2' ] , [ f . getName ( ) for f in system . getFsms ( ) ] )
    def testGetState ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        system = getSystems ( self . app ) . pop ( )
        self . assertEqual ( [ 'initial' , 'initial' ] , [ f . getState ( ) for f in system . getFsms ( ) ] )
    def testSetState ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        system = getSystems ( self . app ) . pop ( )
        fsm1 , fsm2 = system . getFsms ( )
        fsm1 . setState ( 'state1' )
        fsm2 . setState ( 'state2' )
        self . assertEqual ( [ 'state1' , 'state2' ] , [ f . getState ( ) for f in system . getFsms ( ) ] )

class FsmTransitionTestCase ( unittest . TestCase ) :
    def setUp ( self ) :
        config = ''
        config += '<config>\n'
        config += '    <test>\n'
        config += '        <test1>test1</test1>\n'
        config += '        <test2>test2</test2>\n'
        config += '    </test>\n'
        config += '    <system>\n'
        config += '        <name>system1</name>\n'
        config += '        <params>\n'
        config += '            <param1/>\n'
        config += '        </params>\n'
        config += '        <fsm>\n'
        config += '            <name>fsm1</name>\n'
        config += '            <state>\n'
        config += '                <name>initial</name>\n'
        config += '                <on_exit>\n'
        config += '                    <send_message> <name>message1</name> </send_message>\n'
        config += '                </on_exit>\n'
        config += '                <transition>\n'
        config += '                    <to_state>state1</to_state>\n'
        config += '                </transition>\n'
        config += '                <transition>\n'
        config += '                    <to_state>state4</to_state>\n'
        config += '                </transition>\n'
        config += '            </state>\n'
        config += '            <state>\n'
        config += '                <name>state1</name>\n'
        config += '                <on_entry>\n'
        config += '                    <send_message> <name>message2</name> </send_message>\n'
        config += '                </on_entry>\n'
        config += '                <transition>\n'
        config += '                    <inputs> <are_equal> <param>param1</param> <xpath>/world/config/test/test1/text()</xpath> </are_equal> </inputs>\n'
        config += '                    <to_state>state2</to_state>\n'
        config += '                </transition>\n'
        config += '            </state>\n'
        config += '            <state>\n'
        config += '                <name>state2</name>\n'
        config += '                <on_entry>\n'
        config += '                    <send_message> <name>message3</name> </send_message>\n'
        config += '                </on_entry>\n'
        config += '                <transition>\n'
        config += '                    <inputs> <are_equal> <param>param1</param> <xpath>/world/config/test/test2/text()</xpath> </are_equal> </inputs>\n'
        config += '                    <to_state>state3</to_state>\n'
        config += '                </transition>\n'
        config += '            </state>\n'
        config += '            <state>\n'
        config += '                <name>state3</name>\n'
        config += '                <on_entry>\n'
        config += '                    <send_message> <name>message4</name> </send_message>\n'
        config += '                </on_entry>\n'
        config += '            </state>\n'
        config += '            <state>\n'
        config += '                <name>state4</name>\n'
        config += '                <on_entry>\n'
        config += '                    <send_message> <name>message5</name> </send_message>\n'
        config += '                </on_entry>\n'
        config += '            </state>\n'
        config += '        </fsm>\n'
        config += '    </system>\n'
        config += '</config>\n'
        uids = [ 'uid1' ]
        uids . reverse ( )
        uidsProvider = TestUidProvider ( uids )
        self . app = draft . Application ( config = config , uid = uidsProvider )
    def testTransition ( self ) :
        spawnSystems ( self . app , name = 'system1' , params = { 'param1' : [ 'test1' ] } )
        system = getSystems ( self . app ) . pop ( )
        fsm = system . getFsms ( ) . pop ( )
        actions , transition = fsm . transite ( )
        for action in actions :
            action . execute ( )
        transition . changeState ( )
        self . assertEqual ( 'state2' , fsm . getState ( ) )
        self . assertEqual ( [ 'message1' , 'message2' , 'message3' ] , [ m . getName ( ) for m in getMessages ( self . app ) ] )

class FsmInputActionsTestCase ( unittest . TestCase ) :
    def setUp ( self ) :
        config = ''
        config += '<config>\n'
        config += '    <test>\n'
        config += '        <test1>test1</test1>\n'
        config += '        <test2>test2</test2>\n'
        config += '    </test>\n'
        config += '    <system>\n'
        config += '        <name>system1</name>\n'
        config += '        <params>\n'
        config += '            <param1/>\n'
        config += '            <param2/>\n'
        config += '        </params>\n'
        config += '        <fsm>\n'
        config += '            <name>fsm1</name>\n'
        config += '            <state>\n'
        config += '                <name>initial</name>\n'
        config += '                <on_input>\n'
        config += '                    <inputs>\n'
        config += '                        <are_equal> <param>param1</param> <xpath>/world/config/test/test1/text()</xpath> </are_equal>\n'
        config += '                        <are_equal> <param>param2</param> <xpath>/world/config/test/test2/text()</xpath> </are_equal>\n'
        config += '                    </inputs>\n'
        config += '                    <actions>\n'
        config += '                        <send_message> <name>message1</name> </send_message>\n'
        config += '                    </actions>\n'
        config += '                </on_input>\n'
        config += '                <on_input>\n'
        config += '                    <inputs> <are_equal> <param>param1</param> <xpath>/world/config/test/test1/text()</xpath> </are_equal> </inputs>\n'
        config += '                    <inputs> <are_equal> <param>param2</param> <xpath>/world/config/test/test2/text()</xpath> </are_equal> </inputs>\n'
        config += '                    <actions>\n'
        config += '                        <send_message> <name>message2</name> </send_message>\n'
        config += '                    </actions>\n'
        config += '                </on_input>\n'
        config += '            </state>\n'
        config += '        </fsm>\n'
        config += '    </system>\n'
        config += '</config>\n'
        uids = [ 'uid1' ]
        uids . reverse ( )
        uidsProvider = TestUidProvider ( uids )
        self . app = draft . Application ( config = config , uid = uidsProvider )
        spawnSystems ( self . app , name = 'system1' )
        self . system = getSystems ( self . app ) . pop ( )
        self . fsm = self . system . getFsms ( ) . pop ( )
    def setParams ( self , params ) :
        for param , value in params . items ( ) :
            self . system . setParam ( param , value )
    def messagesSent ( self , params ) :
        for msg in getMessages ( self . app ) :
            msg . kill ( )
        self . setParams ( params )
        for action in self . fsm . inputActions ( ) :
            action . execute ( )
        return  [ m . getName ( ) for m in getMessages ( self . app ) ]
    def inputs ( self , params ) :
        self . setParams ( params )
        return self . fsm . computeInputs ( )
    def testInputActions ( self ) :
        self . assertEqual ( [ ]                         , self . messagesSent ( { 'param1' : 'value1' , 'param2' : 'value2' } ) )
        self . assertEqual ( [ 'message2' ]              , self . messagesSent ( { 'param1' : 'test1'  , 'param2' : 'value2' } ) )
        self . assertEqual ( [ 'message2' ]              , self . messagesSent ( { 'param1' : 'value1' , 'param2' : 'test2'  } ) )
        self . assertEqual ( [ 'message1' , 'message2' ] , self . messagesSent ( { 'param1' : 'test1'  , 'param2' : 'test2'  } ) )
    def testComputeInputs ( self ) :
        self . assertEqual ( [ False , False , False , False ] , self . inputs ( { 'param1' : 'value1' , 'param2' : 'value2' } ) )
        self . assertEqual ( [ True  , False , True  , False ] , self . inputs ( { 'param1' : 'test1'  , 'param2' : 'value2' } ) )
        self . assertEqual ( [ True  , True  , True  , True  ] , self . inputs ( { 'param1' : 'test1'  , 'param2' : 'test2'  } ) )
    def testGetInputs ( self ) :
        self . fsm . setInputs ( [ False , True ] )
        self . assertEqual ( [ False , True ] , self . system . getFsms ( ) . pop ( ) . getInputs ( ) )
    def testUpdateInputs ( self ) :
        self . setParams ( { 'param1' : 'test1' , 'param2' : 'test2' } )
        self . fsm . updateInputs ( )
        self . assertEqual ( [ True , True , True , True ] , self . fsm . getInputs ( ) )
    def testInputsChanged ( self ) :
        self . setParams ( { 'param1' : 'test1' , 'param2' : 'test2' } )
        self . fsm . updateInputs ( )
        self . assertEqual ( False , self . fsm . inputsChanged ( ) )
        self . setParams ( { 'param1' : 'value1' , 'param2' : 'value2' } )
        self . assertEqual ( True , self . fsm . inputsChanged ( ) )

class RunSystemsTestCase ( unittest . TestCase ) :
    def setUp ( self ) :
        config = ''
        config += '<config>\n'
        config += '    <test>\n'
        config += '        <test1>test1</test1>\n'
        config += '    </test>\n'
        config += '    <system>\n'
        config += '        <name>system1</name>\n'
        config += '        <params>\n'
        config += '            <param1/>\n'
        config += '        </params>\n'
        config += '        <fsm>\n'
        config += '            <name>fsm1</name>\n'
        config += '            <state>\n'
        config += '                <name>initial</name>\n'
        config += '                <transition>\n'
        config += '                    <to_state>state1</to_state>\n'
        config += '                </transition>\n'
        config += '            </state>\n'
        config += '            <state>\n'
        config += '                <name>state1</name>\n'
        config += '                <on_entry>\n'
        config += '                    <send_message> <name>message1</name> </send_message>\n'
        config += '                    <set_param> <name>param1</name> <value><xpath>/world/config/test/test1/text()</xpath></value> </set_param>\n'
        config += '                </on_entry>\n'
        config += '                <on_input>\n'
        config += '                    <inputs>\n'
        config += '                        <are_equal> <param>param1</param> <xpath>/world/config/test/test1/text()</xpath> </are_equal>\n'
        config += '                    </inputs>\n'
        config += '                    <actions>\n'
        config += '                        <send_message> <name>message3</name> </send_message>\n'
        config += '                    </actions>\n'
        config += '                </on_input>\n'
        config += '                <transition>\n'
        config += '                    <inputs>\n'
        config += '                        <are_equal> <param>param1</param> <xpath>/world/config/test/test1/text()</xpath> </are_equal>\n'
        config += '                    </inputs>\n'
        config += '                    <to_state>state2</to_state>\n'
        config += '                </transition>\n'
        config += '            </state>\n'
        config += '            <state>\n'
        config += '                <name>state2</name>\n'
        config += '                <on_entry>\n'
        config += '                    <send_message> <name>message4</name> </send_message>\n'
        config += '                </on_entry>\n'
        config += '            </state>\n'
        config += '        </fsm>\n'
        config += '    </system>\n'
        config += '    <system>\n'
        config += '        <name>system2</name>\n'
        config += '        <fsm>\n'
        config += '            <name>fsm1</name>\n'
        config += '            <state>\n'
        config += '                <name>initial</name>\n'
        config += '                <transition>\n'
        config += '                    <to_state>state1</to_state>\n'
        config += '                </transition>\n'
        config += '            </state>\n'
        config += '            <state>\n'
        config += '                <name>state1</name>\n'
        config += '                <on_entry>\n'
        config += '                    <send_message> <name>message2</name> </send_message>\n'
        config += '                </on_entry>\n'
        config += '            </state>\n'
        config += '        </fsm>\n'
        config += '    </system>\n'
        config += '</config>\n'
        uids = [ 'uid1' , 'uid2' ]
        uids . reverse ( )
        uidsProvider = TestUidProvider ( uids )
        self . app = draft . Application ( config = config , uid = uidsProvider )
    def testRunSystems ( self ) :
        spawnSystems ( self . app , name = 'system1' )
        spawnSystems ( self . app , name = 'system2' )
        self . app . runSystems ( )
        messages = [ m . getName ( ) for m in getMessages ( self . app ) ]
        self . assertEqual ( [ 'message1' , 'message2' , 'message3' , 'message4' ] , messages )

if __name__ == '__main__' :
    unittest . main ( )
