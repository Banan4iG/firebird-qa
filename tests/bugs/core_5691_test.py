#coding:utf-8

"""
ID:          issue-5957
ISSUE:       5957
TITLE:       File description on Firebird executables should be specific
DESCRIPTION:
  ::: NB :::
  We can not obtain 'File description' property using Python.
  Also this property is not accessible for WMIC interface.
  For this reason it was decided to create on-the-fly Visual Basic script and process it by CSCRIPT.EXE utility
  which exists since 2000/XP on every Windows host in %System%\\system32\\ folder.
  VB script accepts full path and filename as single mandatory argument.
  We run this script for each widely-used FB binaries (executables and DLLs).
  Its output must contain only FILE name (w/o disk and path) and its 'File description' property value.
JIRA:        CORE-5691
FBTEST:      bugs.core_5691
"""

import pytest
from firebird.qa import *

db = db_factory()

act = python_act('db', substitutions=[('[ \\t]+', ' ')])

expected_stdout = """
    'fb_lock_print.exe' 		file description: firebird lock print tool (64-bit)
    'fbclient.dll' 				file description: firebird client library (64-bit)
    'fbguard.exe' 				file description: firebird guardian (64-bit)
    'fbsvcmgr.exe' 				file description: firebird services management tool (64-bit)
    'fbtracemgr.exe' 			file description: firebird trace management tool (64-bit)
    'firebird.exe' 				file description: firebird server executable (64-bit)
    'gbak.exe' 					file description: firebird gbak tool (64-bit)
    'gfix.exe' 					file description: firebird gfix tool (64-bit)
    'gstat.exe' 				file description: firebird gstat tool (64-bit)
    'isql.exe' 					file description: firebird interactive query tool (64-bit)
    'nbackup.exe' 				file description: firebird physical backup management tool (64-bit)
    'chacha.dll' 				file description: firebird wire encryption plugin using chacha cypher (64-bit)
    'engine13.dll' 				file description: firebird engine plugin (64-bit)
    'fbtrace.dll' 				file description: firebird trace plugin (64-bit)
    'legacy_auth.dll' 			file description: firebird legacy auth plugin (64-bit)
    'legacy_usermanager.dll' 	file description: firebird legacy user manager plugin (64-bit)
    'srp.dll' 					file description: firebird srp user manager plugin (64-bit)
    'udr_engine.dll' 			file description: firebird user defined routines engine (64-bit)
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.version('>=4.0')
@pytest.mark.platform('Windows')
def test_1(act: Action):
    pytest.fail("Not IMPLEMENTED")

# test_script_1
#---
# \\
#  import os
#  import subprocess
#  from fdb import services
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  #--------------------------------------------
#  def cleanup( f_names_list ):
#      global os
#      for i in range(len( f_names_list )):
#         if os.path.isfile( f_names_list[i]):
#              os.remove( f_names_list[i] )
#  #--------------------------------------------
#
#  fb_home = services.connect(host='localhost', user= user_name, password= user_password).get_home_directory()
#  db_conn.close()
#
#
#  vbs_cmd = open( os.path.join(context['temp_directory'],'tmp_5691_get_file_descr.vbs'), 'w', buffering = 0)
#
#  vbs_source = \\
#  r'''
#  Option Explicit
#
#  if wscript.arguments.count = 0 then
#      wscript.echo "Missed fully qualified file name, i.e.: drive + path + file_name"
#      wscript.quit
#  end if
#
#  dim fullname
#  dim getDetails
#
#  fullname = wscript.arguments(0)
#
#  rem https://www.tek-tips.com/viewthread.cfm?qid=1402419
#
#  getDetails = GetFileDetails( fullName )
#
#
#  function GetFileDetails(fullName)
#
#      on error resume next
#
#      dim fso
#      dim objFile
#
#      set fso = CreateObject("Scripting.FileSystemObject")
#      set objFile = fso.GetFile(fullName)
#
#      if not fso.FileExists(fullName) Then
#          wscript.echo "File '" & fullName & "' does not exist."
#          wscript.Quit
#      end if
#
#      dim fileName
#      dim folderName
#
#      fileName = objFile.Name
#      folderName = objFile.Path
#      folderName = Left(folderName, Len(folderName)-Len(fileName))
#
#      set objFile = Nothing
#      set fso = Nothing
#
#      dim objShell
#      dim objFolder
#
#      rem https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/bb776890(v=vs.85)
#      rem The Windows Shell provides a powerful set of automation objects <...>
#      rem You can use these objects to access <...> the file system, launch programs, and change system settings.
#
#      set objShell = CreateObject("Shell.Application")
#      set objFolder = objShell.NameSpace(folderName)
#
#  	dim i
#      dim fdescr_idx
#      dim propertyName
#
#  	i = 0
#  	fdescr_idx = 0
#  	do
#  		propertyName = vbNullString
#  		rem https://docs.microsoft.com/en-us/windows/win32/shell/folder-getdetailsof
#  		rem retrieves details about an item in a folder. for example, its size, type, or the time of its last modification.
#  		propertyName = objFolder.GetDetailsOf(objFolder.Items, i)
#  		if LCase(propertyName) = LCase("file description") then
#  			fdescr_idx = i
#  			exit do
#  		end if
#
#  		if propertyName = vbNullString then
#  			exit do
#  		end if
#  		i = i + 1
#  	loop
#  	propertyName = Nothing
#  	rem wscript.echo "fdescr_idx=",fdescr_idx
#
#  	dim objFolderItem
#  	set objFolderItem = objFolder.ParseName(fileName)
#
#  	if (not objFolderItem Is Nothing) then
#  	    dim attribName
#  		dim objInfo
#  		attribName = objFolder.GetDetailsOf(objFolder.Items, fdescr_idx)
#  		objInfo = objFolder.GetDetailsOf(objFolderItem, fdescr_idx)
#
#  		wscript.echo "'" & fileName & "' " & LCase(attribName) & ":", LCase(objInfo)
#
#  	    attribName = Nothing
#  		objInfo = Nothing
#  	end if
#
#  	set objFolderItem = Nothing
#      set objFolder = Nothing
#      set objShell = Nothing
#  end function
#  '''
#
#  vbs_cmd.write(vbs_source)
#  vbs_cmd.close()
#
#  vbs_log = open( os.path.join(context['temp_directory'],'tmp_5691_get_file_descr.log'), 'w', buffering = 0)
#  vbs_err = open( os.path.join(context['temp_directory'],'tmp_5691_get_file_descr.err'), 'w', buffering = 0)
#
#  f_list = ( 'fbclient.dll',
#             'gbak.exe',
#             'gfix.exe',
#             'gstat.exe',
#             'fbguard.exe',
#             'isql.exe',
#             'fb_lock_print.exe',
#             'firebird.exe',
#             'nbackup.exe',
#             'fbtracemgr.exe',
#             'fbsvcmgr.exe',
#             r'plugins\\engine13.dll',
#             r'plugins\\legacy_auth.dll',
#             r'plugins\\legacy_usermanager.dll',
#             r'plugins\\srp.dll',
#             r'plugins\\udr_engine.dll',
#             r'plugins\\chacha.dll',
#             r'plugins\\\\fbtrace.dll',
#           )
#  for x in sorted(f_list):
#      subprocess.call( [ 'cscript', '//nologo', vbs_cmd.name, ''.join( (fb_home, x) )  ], stdout = vbs_log, stderr = vbs_err )
#
#  vbs_log.close()
#  vbs_err.close()
#
#  with open( vbs_err.name,'r') as f:
#      for line in f:
#          print("Unexpected STDERR, file "+vbs_err.name+": " + line)
#
#  with open( vbs_log.name,'r') as f:
#      for line in f:
#          print( line.lower() )
#
#  os.remove( vbs_log.name )
#  os.remove( vbs_err.name )
#  os.remove( vbs_cmd.name )
#
#
#---
