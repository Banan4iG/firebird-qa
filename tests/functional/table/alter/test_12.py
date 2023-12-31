#coding:utf-8

"""
ID:          table.alter-12
TITLE:       Verify ability to create exactly 254 changes of format (increasing it by 1) after initial creating table
DESCRIPTION: 
FBTEST:      functional.table.alter.12
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    recreate table test1(f0 int); -- this also create "format #1"
    -- following shoudl run OK because of 254 changes:
    alter table test1 add f1 int;
    alter table test1 add f2 int;
    alter table test1 add f3 int;
    alter table test1 add f4 int;
    alter table test1 add f5 int;
    alter table test1 add f6 int;
    alter table test1 add f7 int;
    alter table test1 add f8 int;
    alter table test1 add f9 int;
    alter table test1 add f10 int;
    alter table test1 add f11 int;
    alter table test1 add f12 int;
    alter table test1 add f13 int;
    alter table test1 add f14 int;
    alter table test1 add f15 int;
    alter table test1 add f16 int;
    alter table test1 add f17 int;
    alter table test1 add f18 int;
    alter table test1 add f19 int;
    alter table test1 add f20 int;
    alter table test1 add f21 int;
    alter table test1 add f22 int;
    alter table test1 add f23 int;
    alter table test1 add f24 int;
    alter table test1 add f25 int;
    alter table test1 add f26 int;
    alter table test1 add f27 int;
    alter table test1 add f28 int;
    alter table test1 add f29 int;
    alter table test1 add f30 int;
    alter table test1 add f31 int;
    alter table test1 add f32 int;
    alter table test1 add f33 int;
    alter table test1 add f34 int;
    alter table test1 add f35 int;
    alter table test1 add f36 int;
    alter table test1 add f37 int;
    alter table test1 add f38 int;
    alter table test1 add f39 int;
    alter table test1 add f40 int;
    alter table test1 add f41 int;
    alter table test1 add f42 int;
    alter table test1 add f43 int;
    alter table test1 add f44 int;
    alter table test1 add f45 int;
    alter table test1 add f46 int;
    alter table test1 add f47 int;
    alter table test1 add f48 int;
    alter table test1 add f49 int;
    alter table test1 add f50 int;
    alter table test1 add f51 int;
    alter table test1 add f52 int;
    alter table test1 add f53 int;
    alter table test1 add f54 int;
    alter table test1 add f55 int;
    alter table test1 add f56 int;
    alter table test1 add f57 int;
    alter table test1 add f58 int;
    alter table test1 add f59 int;
    alter table test1 add f60 int;
    alter table test1 add f61 int;
    alter table test1 add f62 int;
    alter table test1 add f63 int;
    alter table test1 add f64 int;
    alter table test1 add f65 int;
    alter table test1 add f66 int;
    alter table test1 add f67 int;
    alter table test1 add f68 int;
    alter table test1 add f69 int;
    alter table test1 add f70 int;
    alter table test1 add f71 int;
    alter table test1 add f72 int;
    alter table test1 add f73 int;
    alter table test1 add f74 int;
    alter table test1 add f75 int;
    alter table test1 add f76 int;
    alter table test1 add f77 int;
    alter table test1 add f78 int;
    alter table test1 add f79 int;
    alter table test1 add f80 int;
    alter table test1 add f81 int;
    alter table test1 add f82 int;
    alter table test1 add f83 int;
    alter table test1 add f84 int;
    alter table test1 add f85 int;
    alter table test1 add f86 int;
    alter table test1 add f87 int;
    alter table test1 add f88 int;
    alter table test1 add f89 int;
    alter table test1 add f90 int;
    alter table test1 add f91 int;
    alter table test1 add f92 int;
    alter table test1 add f93 int;
    alter table test1 add f94 int;
    alter table test1 add f95 int;
    alter table test1 add f96 int;
    alter table test1 add f97 int;
    alter table test1 add f98 int;
    alter table test1 add f99 int;
    alter table test1 add f100 int;
    alter table test1 add f101 int;
    alter table test1 add f102 int;
    alter table test1 add f103 int;
    alter table test1 add f104 int;
    alter table test1 add f105 int;
    alter table test1 add f106 int;
    alter table test1 add f107 int;
    alter table test1 add f108 int;
    alter table test1 add f109 int;
    alter table test1 add f110 int;
    alter table test1 add f111 int;
    alter table test1 add f112 int;
    alter table test1 add f113 int;
    alter table test1 add f114 int;
    alter table test1 add f115 int;
    alter table test1 add f116 int;
    alter table test1 add f117 int;
    alter table test1 add f118 int;
    alter table test1 add f119 int;
    alter table test1 add f120 int;
    alter table test1 add f121 int;
    alter table test1 add f122 int;
    alter table test1 add f123 int;
    alter table test1 add f124 int;
    alter table test1 add f125 int;
    alter table test1 add f126 int;
    alter table test1 add f127 int;
    alter table test1 add f128 int;
    alter table test1 add f129 int;
    alter table test1 add f130 int;
    alter table test1 add f131 int;
    alter table test1 add f132 int;
    alter table test1 add f133 int;
    alter table test1 add f134 int;
    alter table test1 add f135 int;
    alter table test1 add f136 int;
    alter table test1 add f137 int;
    alter table test1 add f138 int;
    alter table test1 add f139 int;
    alter table test1 add f140 int;
    alter table test1 add f141 int;
    alter table test1 add f142 int;
    alter table test1 add f143 int;
    alter table test1 add f144 int;
    alter table test1 add f145 int;
    alter table test1 add f146 int;
    alter table test1 add f147 int;
    alter table test1 add f148 int;
    alter table test1 add f149 int;
    alter table test1 add f150 int;
    alter table test1 add f151 int;
    alter table test1 add f152 int;
    alter table test1 add f153 int;
    alter table test1 add f154 int;
    alter table test1 add f155 int;
    alter table test1 add f156 int;
    alter table test1 add f157 int;
    alter table test1 add f158 int;
    alter table test1 add f159 int;
    alter table test1 add f160 int;
    alter table test1 add f161 int;
    alter table test1 add f162 int;
    alter table test1 add f163 int;
    alter table test1 add f164 int;
    alter table test1 add f165 int;
    alter table test1 add f166 int;
    alter table test1 add f167 int;
    alter table test1 add f168 int;
    alter table test1 add f169 int;
    alter table test1 add f170 int;
    alter table test1 add f171 int;
    alter table test1 add f172 int;
    alter table test1 add f173 int;
    alter table test1 add f174 int;
    alter table test1 add f175 int;
    alter table test1 add f176 int;
    alter table test1 add f177 int;
    alter table test1 add f178 int;
    alter table test1 add f179 int;
    alter table test1 add f180 int;
    alter table test1 add f181 int;
    alter table test1 add f182 int;
    alter table test1 add f183 int;
    alter table test1 add f184 int;
    alter table test1 add f185 int;
    alter table test1 add f186 int;
    alter table test1 add f187 int;
    alter table test1 add f188 int;
    alter table test1 add f189 int;
    alter table test1 add f190 int;
    alter table test1 add f191 int;
    alter table test1 add f192 int;
    alter table test1 add f193 int;
    alter table test1 add f194 int;
    alter table test1 add f195 int;
    alter table test1 add f196 int;
    alter table test1 add f197 int;
    alter table test1 add f198 int;
    alter table test1 add f199 int;
    alter table test1 add f200 int;
    alter table test1 add f201 int;
    alter table test1 add f202 int;
    alter table test1 add f203 int;
    alter table test1 add f204 int;
    alter table test1 add f205 int;
    alter table test1 add f206 int;
    alter table test1 add f207 int;
    alter table test1 add f208 int;
    alter table test1 add f209 int;
    alter table test1 add f210 int;
    alter table test1 add f211 int;
    alter table test1 add f212 int;
    alter table test1 add f213 int;
    alter table test1 add f214 int;
    alter table test1 add f215 int;
    alter table test1 add f216 int;
    alter table test1 add f217 int;
    alter table test1 add f218 int;
    alter table test1 add f219 int;
    alter table test1 add f220 int;
    alter table test1 add f221 int;
    alter table test1 add f222 int;
    alter table test1 add f223 int;
    alter table test1 add f224 int;
    alter table test1 add f225 int;
    alter table test1 add f226 int;
    alter table test1 add f227 int;
    alter table test1 add f228 int;
    alter table test1 add f229 int;
    alter table test1 add f230 int;
    alter table test1 add f231 int;
    alter table test1 add f232 int;
    alter table test1 add f233 int;
    alter table test1 add f234 int;
    alter table test1 add f235 int;
    alter table test1 add f236 int;
    alter table test1 add f237 int;
    alter table test1 add f238 int;
    alter table test1 add f239 int;
    alter table test1 add f240 int;
    alter table test1 add f241 int;
    alter table test1 add f242 int;
    alter table test1 add f243 int;
    alter table test1 add f244 int;
    alter table test1 add f245 int;
    alter table test1 add f246 int;
    alter table test1 add f247 int;
    alter table test1 add f248 int;
    alter table test1 add f249 int;
    alter table test1 add f250 int;
    alter table test1 add f251 int;
    alter table test1 add f252 int;
    alter table test1 add f253 int;
    alter table test1 add f254 int;
    commit;

    show table test1;

    -- following shoudl FAIL because of 255 changes:
    recreate table test2(f0 int);
    alter table test2 add f1 int;
    alter table test2 add f2 int;
    alter table test2 add f3 int;
    alter table test2 add f4 int;
    alter table test2 add f5 int;
    alter table test2 add f6 int;
    alter table test2 add f7 int;
    alter table test2 add f8 int;
    alter table test2 add f9 int;
    alter table test2 add f10 int;
    alter table test2 add f11 int;
    alter table test2 add f12 int;
    alter table test2 add f13 int;
    alter table test2 add f14 int;
    alter table test2 add f15 int;
    alter table test2 add f16 int;
    alter table test2 add f17 int;
    alter table test2 add f18 int;
    alter table test2 add f19 int;
    alter table test2 add f20 int;
    alter table test2 add f21 int;
    alter table test2 add f22 int;
    alter table test2 add f23 int;
    alter table test2 add f24 int;
    alter table test2 add f25 int;
    alter table test2 add f26 int;
    alter table test2 add f27 int;
    alter table test2 add f28 int;
    alter table test2 add f29 int;
    alter table test2 add f30 int;
    alter table test2 add f31 int;
    alter table test2 add f32 int;
    alter table test2 add f33 int;
    alter table test2 add f34 int;
    alter table test2 add f35 int;
    alter table test2 add f36 int;
    alter table test2 add f37 int;
    alter table test2 add f38 int;
    alter table test2 add f39 int;
    alter table test2 add f40 int;
    alter table test2 add f41 int;
    alter table test2 add f42 int;
    alter table test2 add f43 int;
    alter table test2 add f44 int;
    alter table test2 add f45 int;
    alter table test2 add f46 int;
    alter table test2 add f47 int;
    alter table test2 add f48 int;
    alter table test2 add f49 int;
    alter table test2 add f50 int;
    alter table test2 add f51 int;
    alter table test2 add f52 int;
    alter table test2 add f53 int;
    alter table test2 add f54 int;
    alter table test2 add f55 int;
    alter table test2 add f56 int;
    alter table test2 add f57 int;
    alter table test2 add f58 int;
    alter table test2 add f59 int;
    alter table test2 add f60 int;
    alter table test2 add f61 int;
    alter table test2 add f62 int;
    alter table test2 add f63 int;
    alter table test2 add f64 int;
    alter table test2 add f65 int;
    alter table test2 add f66 int;
    alter table test2 add f67 int;
    alter table test2 add f68 int;
    alter table test2 add f69 int;
    alter table test2 add f70 int;
    alter table test2 add f71 int;
    alter table test2 add f72 int;
    alter table test2 add f73 int;
    alter table test2 add f74 int;
    alter table test2 add f75 int;
    alter table test2 add f76 int;
    alter table test2 add f77 int;
    alter table test2 add f78 int;
    alter table test2 add f79 int;
    alter table test2 add f80 int;
    alter table test2 add f81 int;
    alter table test2 add f82 int;
    alter table test2 add f83 int;
    alter table test2 add f84 int;
    alter table test2 add f85 int;
    alter table test2 add f86 int;
    alter table test2 add f87 int;
    alter table test2 add f88 int;
    alter table test2 add f89 int;
    alter table test2 add f90 int;
    alter table test2 add f91 int;
    alter table test2 add f92 int;
    alter table test2 add f93 int;
    alter table test2 add f94 int;
    alter table test2 add f95 int;
    alter table test2 add f96 int;
    alter table test2 add f97 int;
    alter table test2 add f98 int;
    alter table test2 add f99 int;
    alter table test2 add f100 int;
    alter table test2 add f101 int;
    alter table test2 add f102 int;
    alter table test2 add f103 int;
    alter table test2 add f104 int;
    alter table test2 add f105 int;
    alter table test2 add f106 int;
    alter table test2 add f107 int;
    alter table test2 add f108 int;
    alter table test2 add f109 int;
    alter table test2 add f110 int;
    alter table test2 add f111 int;
    alter table test2 add f112 int;
    alter table test2 add f113 int;
    alter table test2 add f114 int;
    alter table test2 add f115 int;
    alter table test2 add f116 int;
    alter table test2 add f117 int;
    alter table test2 add f118 int;
    alter table test2 add f119 int;
    alter table test2 add f120 int;
    alter table test2 add f121 int;
    alter table test2 add f122 int;
    alter table test2 add f123 int;
    alter table test2 add f124 int;
    alter table test2 add f125 int;
    alter table test2 add f126 int;
    alter table test2 add f127 int;
    alter table test2 add f128 int;
    alter table test2 add f129 int;
    alter table test2 add f130 int;
    alter table test2 add f131 int;
    alter table test2 add f132 int;
    alter table test2 add f133 int;
    alter table test2 add f134 int;
    alter table test2 add f135 int;
    alter table test2 add f136 int;
    alter table test2 add f137 int;
    alter table test2 add f138 int;
    alter table test2 add f139 int;
    alter table test2 add f140 int;
    alter table test2 add f141 int;
    alter table test2 add f142 int;
    alter table test2 add f143 int;
    alter table test2 add f144 int;
    alter table test2 add f145 int;
    alter table test2 add f146 int;
    alter table test2 add f147 int;
    alter table test2 add f148 int;
    alter table test2 add f149 int;
    alter table test2 add f150 int;
    alter table test2 add f151 int;
    alter table test2 add f152 int;
    alter table test2 add f153 int;
    alter table test2 add f154 int;
    alter table test2 add f155 int;
    alter table test2 add f156 int;
    alter table test2 add f157 int;
    alter table test2 add f158 int;
    alter table test2 add f159 int;
    alter table test2 add f160 int;
    alter table test2 add f161 int;
    alter table test2 add f162 int;
    alter table test2 add f163 int;
    alter table test2 add f164 int;
    alter table test2 add f165 int;
    alter table test2 add f166 int;
    alter table test2 add f167 int;
    alter table test2 add f168 int;
    alter table test2 add f169 int;
    alter table test2 add f170 int;
    alter table test2 add f171 int;
    alter table test2 add f172 int;
    alter table test2 add f173 int;
    alter table test2 add f174 int;
    alter table test2 add f175 int;
    alter table test2 add f176 int;
    alter table test2 add f177 int;
    alter table test2 add f178 int;
    alter table test2 add f179 int;
    alter table test2 add f180 int;
    alter table test2 add f181 int;
    alter table test2 add f182 int;
    alter table test2 add f183 int;
    alter table test2 add f184 int;
    alter table test2 add f185 int;
    alter table test2 add f186 int;
    alter table test2 add f187 int;
    alter table test2 add f188 int;
    alter table test2 add f189 int;
    alter table test2 add f190 int;
    alter table test2 add f191 int;
    alter table test2 add f192 int;
    alter table test2 add f193 int;
    alter table test2 add f194 int;
    alter table test2 add f195 int;
    alter table test2 add f196 int;
    alter table test2 add f197 int;
    alter table test2 add f198 int;
    alter table test2 add f199 int;
    alter table test2 add f200 int;
    alter table test2 add f201 int;
    alter table test2 add f202 int;
    alter table test2 add f203 int;
    alter table test2 add f204 int;
    alter table test2 add f205 int;
    alter table test2 add f206 int;
    alter table test2 add f207 int;
    alter table test2 add f208 int;
    alter table test2 add f209 int;
    alter table test2 add f210 int;
    alter table test2 add f211 int;
    alter table test2 add f212 int;
    alter table test2 add f213 int;
    alter table test2 add f214 int;
    alter table test2 add f215 int;
    alter table test2 add f216 int;
    alter table test2 add f217 int;
    alter table test2 add f218 int;
    alter table test2 add f219 int;
    alter table test2 add f220 int;
    alter table test2 add f221 int;
    alter table test2 add f222 int;
    alter table test2 add f223 int;
    alter table test2 add f224 int;
    alter table test2 add f225 int;
    alter table test2 add f226 int;
    alter table test2 add f227 int;
    alter table test2 add f228 int;
    alter table test2 add f229 int;
    alter table test2 add f230 int;
    alter table test2 add f231 int;
    alter table test2 add f232 int;
    alter table test2 add f233 int;
    alter table test2 add f234 int;
    alter table test2 add f235 int;
    alter table test2 add f236 int;
    alter table test2 add f237 int;
    alter table test2 add f238 int;
    alter table test2 add f239 int;
    alter table test2 add f240 int;
    alter table test2 add f241 int;
    alter table test2 add f242 int;
    alter table test2 add f243 int;
    alter table test2 add f244 int;
    alter table test2 add f245 int;
    alter table test2 add f246 int;
    alter table test2 add f247 int;
    alter table test2 add f248 int;
    alter table test2 add f249 int;
    alter table test2 add f250 int;
    alter table test2 add f251 int;
    alter table test2 add f252 int;
    alter table test2 add f253 int;
    alter table test2 add f254 int;
    alter table test2 add f255 int;
    commit;
"""

act = isql_act('db', test_script)

expected_stdout = """
    F0                              INTEGER Nullable 
    F1                              INTEGER Nullable 
    F2                              INTEGER Nullable 
    F3                              INTEGER Nullable 
    F4                              INTEGER Nullable 
    F5                              INTEGER Nullable 
    F6                              INTEGER Nullable 
    F7                              INTEGER Nullable 
    F8                              INTEGER Nullable 
    F9                              INTEGER Nullable 
    F10                             INTEGER Nullable 
    F11                             INTEGER Nullable 
    F12                             INTEGER Nullable 
    F13                             INTEGER Nullable 
    F14                             INTEGER Nullable 
    F15                             INTEGER Nullable 
    F16                             INTEGER Nullable 
    F17                             INTEGER Nullable 
    F18                             INTEGER Nullable 
    F19                             INTEGER Nullable 
    F20                             INTEGER Nullable 
    F21                             INTEGER Nullable 
    F22                             INTEGER Nullable 
    F23                             INTEGER Nullable 
    F24                             INTEGER Nullable 
    F25                             INTEGER Nullable 
    F26                             INTEGER Nullable 
    F27                             INTEGER Nullable 
    F28                             INTEGER Nullable 
    F29                             INTEGER Nullable 
    F30                             INTEGER Nullable 
    F31                             INTEGER Nullable 
    F32                             INTEGER Nullable 
    F33                             INTEGER Nullable 
    F34                             INTEGER Nullable 
    F35                             INTEGER Nullable 
    F36                             INTEGER Nullable 
    F37                             INTEGER Nullable 
    F38                             INTEGER Nullable 
    F39                             INTEGER Nullable 
    F40                             INTEGER Nullable 
    F41                             INTEGER Nullable 
    F42                             INTEGER Nullable 
    F43                             INTEGER Nullable 
    F44                             INTEGER Nullable 
    F45                             INTEGER Nullable 
    F46                             INTEGER Nullable 
    F47                             INTEGER Nullable 
    F48                             INTEGER Nullable 
    F49                             INTEGER Nullable 
    F50                             INTEGER Nullable 
    F51                             INTEGER Nullable 
    F52                             INTEGER Nullable 
    F53                             INTEGER Nullable 
    F54                             INTEGER Nullable 
    F55                             INTEGER Nullable 
    F56                             INTEGER Nullable 
    F57                             INTEGER Nullable 
    F58                             INTEGER Nullable 
    F59                             INTEGER Nullable 
    F60                             INTEGER Nullable 
    F61                             INTEGER Nullable 
    F62                             INTEGER Nullable 
    F63                             INTEGER Nullable 
    F64                             INTEGER Nullable 
    F65                             INTEGER Nullable 
    F66                             INTEGER Nullable 
    F67                             INTEGER Nullable 
    F68                             INTEGER Nullable 
    F69                             INTEGER Nullable 
    F70                             INTEGER Nullable 
    F71                             INTEGER Nullable 
    F72                             INTEGER Nullable 
    F73                             INTEGER Nullable 
    F74                             INTEGER Nullable 
    F75                             INTEGER Nullable 
    F76                             INTEGER Nullable 
    F77                             INTEGER Nullable 
    F78                             INTEGER Nullable 
    F79                             INTEGER Nullable 
    F80                             INTEGER Nullable 
    F81                             INTEGER Nullable 
    F82                             INTEGER Nullable 
    F83                             INTEGER Nullable 
    F84                             INTEGER Nullable 
    F85                             INTEGER Nullable 
    F86                             INTEGER Nullable 
    F87                             INTEGER Nullable 
    F88                             INTEGER Nullable 
    F89                             INTEGER Nullable 
    F90                             INTEGER Nullable 
    F91                             INTEGER Nullable 
    F92                             INTEGER Nullable 
    F93                             INTEGER Nullable 
    F94                             INTEGER Nullable 
    F95                             INTEGER Nullable 
    F96                             INTEGER Nullable 
    F97                             INTEGER Nullable 
    F98                             INTEGER Nullable 
    F99                             INTEGER Nullable 
    F100                            INTEGER Nullable 
    F101                            INTEGER Nullable 
    F102                            INTEGER Nullable 
    F103                            INTEGER Nullable 
    F104                            INTEGER Nullable 
    F105                            INTEGER Nullable 
    F106                            INTEGER Nullable 
    F107                            INTEGER Nullable 
    F108                            INTEGER Nullable 
    F109                            INTEGER Nullable 
    F110                            INTEGER Nullable 
    F111                            INTEGER Nullable 
    F112                            INTEGER Nullable 
    F113                            INTEGER Nullable 
    F114                            INTEGER Nullable 
    F115                            INTEGER Nullable 
    F116                            INTEGER Nullable 
    F117                            INTEGER Nullable 
    F118                            INTEGER Nullable 
    F119                            INTEGER Nullable 
    F120                            INTEGER Nullable 
    F121                            INTEGER Nullable 
    F122                            INTEGER Nullable 
    F123                            INTEGER Nullable 
    F124                            INTEGER Nullable 
    F125                            INTEGER Nullable 
    F126                            INTEGER Nullable 
    F127                            INTEGER Nullable 
    F128                            INTEGER Nullable 
    F129                            INTEGER Nullable 
    F130                            INTEGER Nullable 
    F131                            INTEGER Nullable 
    F132                            INTEGER Nullable 
    F133                            INTEGER Nullable 
    F134                            INTEGER Nullable 
    F135                            INTEGER Nullable 
    F136                            INTEGER Nullable 
    F137                            INTEGER Nullable 
    F138                            INTEGER Nullable 
    F139                            INTEGER Nullable 
    F140                            INTEGER Nullable 
    F141                            INTEGER Nullable 
    F142                            INTEGER Nullable 
    F143                            INTEGER Nullable 
    F144                            INTEGER Nullable 
    F145                            INTEGER Nullable 
    F146                            INTEGER Nullable 
    F147                            INTEGER Nullable 
    F148                            INTEGER Nullable 
    F149                            INTEGER Nullable 
    F150                            INTEGER Nullable 
    F151                            INTEGER Nullable 
    F152                            INTEGER Nullable 
    F153                            INTEGER Nullable 
    F154                            INTEGER Nullable 
    F155                            INTEGER Nullable 
    F156                            INTEGER Nullable 
    F157                            INTEGER Nullable 
    F158                            INTEGER Nullable 
    F159                            INTEGER Nullable 
    F160                            INTEGER Nullable 
    F161                            INTEGER Nullable 
    F162                            INTEGER Nullable 
    F163                            INTEGER Nullable 
    F164                            INTEGER Nullable 
    F165                            INTEGER Nullable 
    F166                            INTEGER Nullable 
    F167                            INTEGER Nullable 
    F168                            INTEGER Nullable 
    F169                            INTEGER Nullable 
    F170                            INTEGER Nullable 
    F171                            INTEGER Nullable 
    F172                            INTEGER Nullable 
    F173                            INTEGER Nullable 
    F174                            INTEGER Nullable 
    F175                            INTEGER Nullable 
    F176                            INTEGER Nullable 
    F177                            INTEGER Nullable 
    F178                            INTEGER Nullable 
    F179                            INTEGER Nullable 
    F180                            INTEGER Nullable 
    F181                            INTEGER Nullable 
    F182                            INTEGER Nullable 
    F183                            INTEGER Nullable 
    F184                            INTEGER Nullable 
    F185                            INTEGER Nullable 
    F186                            INTEGER Nullable 
    F187                            INTEGER Nullable 
    F188                            INTEGER Nullable 
    F189                            INTEGER Nullable 
    F190                            INTEGER Nullable 
    F191                            INTEGER Nullable 
    F192                            INTEGER Nullable 
    F193                            INTEGER Nullable 
    F194                            INTEGER Nullable 
    F195                            INTEGER Nullable 
    F196                            INTEGER Nullable 
    F197                            INTEGER Nullable 
    F198                            INTEGER Nullable 
    F199                            INTEGER Nullable 
    F200                            INTEGER Nullable 
    F201                            INTEGER Nullable 
    F202                            INTEGER Nullable 
    F203                            INTEGER Nullable 
    F204                            INTEGER Nullable 
    F205                            INTEGER Nullable 
    F206                            INTEGER Nullable 
    F207                            INTEGER Nullable 
    F208                            INTEGER Nullable 
    F209                            INTEGER Nullable 
    F210                            INTEGER Nullable 
    F211                            INTEGER Nullable 
    F212                            INTEGER Nullable 
    F213                            INTEGER Nullable 
    F214                            INTEGER Nullable 
    F215                            INTEGER Nullable 
    F216                            INTEGER Nullable 
    F217                            INTEGER Nullable 
    F218                            INTEGER Nullable 
    F219                            INTEGER Nullable 
    F220                            INTEGER Nullable 
    F221                            INTEGER Nullable 
    F222                            INTEGER Nullable 
    F223                            INTEGER Nullable 
    F224                            INTEGER Nullable 
    F225                            INTEGER Nullable 
    F226                            INTEGER Nullable 
    F227                            INTEGER Nullable 
    F228                            INTEGER Nullable 
    F229                            INTEGER Nullable 
    F230                            INTEGER Nullable 
    F231                            INTEGER Nullable 
    F232                            INTEGER Nullable 
    F233                            INTEGER Nullable 
    F234                            INTEGER Nullable 
    F235                            INTEGER Nullable 
    F236                            INTEGER Nullable 
    F237                            INTEGER Nullable 
    F238                            INTEGER Nullable 
    F239                            INTEGER Nullable 
    F240                            INTEGER Nullable 
    F241                            INTEGER Nullable 
    F242                            INTEGER Nullable 
    F243                            INTEGER Nullable 
    F244                            INTEGER Nullable 
    F245                            INTEGER Nullable 
    F246                            INTEGER Nullable 
    F247                            INTEGER Nullable 
    F248                            INTEGER Nullable 
    F249                            INTEGER Nullable 
    F250                            INTEGER Nullable 
    F251                            INTEGER Nullable 
    F252                            INTEGER Nullable 
    F253                            INTEGER Nullable 
    F254                            INTEGER Nullable 
"""

expected_stderr = """
    Statement failed, SQLSTATE = 54000
    unsuccessful metadata update
    -TABLE TEST2
    -too many versions
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr
    act.execute()
    assert (act.clean_stdout == act.clean_expected_stdout and
            act.clean_stderr == act.clean_expected_stderr)
