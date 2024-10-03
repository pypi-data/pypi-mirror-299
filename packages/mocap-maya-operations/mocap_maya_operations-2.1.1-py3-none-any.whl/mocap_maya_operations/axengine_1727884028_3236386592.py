class WupiError(Exception):
    pass


class WupiLicenseError(WupiError):
    pass


from enum import IntEnum


def _axe_init():
    import ctypes as _c


    class Interface(_c.Structure):
        _fields_ = [('a', _c.c_uint), ('b', _c.c_uint), ('c', _c.c_char_p),
            ('d', _c.c_longlong), ('e', _c.c_longlong)]
    import base64
    buffer = base64.b85decode(__axe_data)
    interface = None
    errorList = []
    _axe_init.cpsrt = _loadCpsRT(errorList)
    if _axe_init.cpsrt == None:
        raise RuntimeError('Could not load cpsrt library:\n' +
            _formatErrorList(errorList))
    import os as _os
    interface = Interface()
    interface.a = 2
    interface.b = 10
    interface.c = buffer
    interface.d = len(buffer)
    interface.e = 0
    _axe_init.cpsrt.Init(_c.byref(interface, 0))
    if interface.e == 0:
        raise RuntimeError('Could not initialize cpsrt session')


class WupiErrorCode(IntEnum):
    WupiErrorNoError = 0,
    WupiErrorLicenseNotFound = -2,
    WupiErrorStateIdOverflow = -16,
    WupiErrorNoBlurryBoxHandleAvailable = -17,
    WupiErrorCodeMovingFunctionNotFound = -21,
    WupiErrorUnitCounterDecrementOutOfRange = -22,
    WupiErrorInternal = -23,
    WupiErrorNotPossible = -24,
    WupiErrorInvalidParameter = -25,
    WupiErrorWibuCmNotRegistered = -26,
    WupiErrorNotImplemented = -100


import os as _os
import sys as _sys


def _getWibuPath():
    return _os.environ.get('WIBU_LIBRARY_PATH')


def _addWibuPath(array):
    wibuLibPath = _getWibuPath()
    if wibuLibPath is not None:
        array.insert(0, _os.path.normpath(wibuLibPath) + '/')


def _is64Bit():
    import struct
    return struct.calcsize('P') == 8


def _isArm():
    try:
        return _os.uname().machine == 'armv7l'
    except:
        return False


def _isArm64():
    try:
        return _os.uname().machine == 'aarch64' or _os.uname(
            ).machine == 'arm64' or _os.uname().machine.startswith('arm'
            ) and _is64Bit()
    except:
        return False


def _isWindows():
    return _sys.platform == 'win32' or _sys.platform == 'cygwin'


def _isLinux():
    return _sys.platform == 'linux'


def _isMacOS():
    return _sys.platform == 'darwin'


def _getLibraryExtension():
    if _isWindows():
        return 'dll'
    if _isMacOS():
        return 'dylib'
    return 'so'


def _getLibraryArchitecture():
    if _isWindows():
        if _is64Bit():
            return '64'
        else:
            return '32'
    else:
        return ''


def _getLibrarySuffix():
    return _getLibraryArchitecture() + '.' + _getLibraryExtension()


def _getLibraryPrefix():
    if _isWindows():
        return ''
    else:
        return 'lib'


def _buildWibuDLLName(dll):
    return _getLibraryPrefix() + dll + _getLibrarySuffix()


def _getSDKPaths(result):
    if _isWindows():
        axProtectorSdk = _os.environ.get('AXPROTECTOR_SDK')
        if axProtectorSdk is not None:
            result.append(axProtectorSdk + 'bin/')
        programFiles = _os.environ.get('ProgramFiles')
        if programFiles is not None:
            result.append(programFiles +
                '/WIBU-SYSTEMS/AxProtector/Devkit/bin/')


def _getDllPaths():
    result = [_os.path.dirname(_os.path.abspath(__file__)) + '/', '']
    _addWibuPath(result)
    _getSDKPaths(result)
    if _isMacOS():
        result.append('/usr/local/lib/')
    return result


def _tryLoadLibrary(file, errorList):
    try:
        import ctypes
        if file.startswith('/') and not _os.path.exists(file):
            return None
        library = ctypes.cdll.LoadLibrary(file)
        return library
    except Exception as e:
        if errorList != None:
            errorList.append([file, e])
        return None


def _loadDLL(dllName, errorList=None):
    dllPaths = _getDllPaths()
    for path in dllPaths:
        file = path + dllName
        library = _tryLoadLibrary(file, errorList)
        if library is not None:
            return library
    return None


def _loadWibuDLL(dll, errorList=None):
    return _loadDLL(_buildWibuDLLName(dll), errorList)


def _getCpsRTSdkPaths():
    result = []
    arch = 'x86'
    if _is64Bit():
        arch = 'x64'
    if _isArm():
        arch = 'armhf'
    if _isArm64():
        arch = 'aarch64'
    _current_os = 'win'
    if _isLinux():
        _current_os = 'lin'
    if _isMacOS():
        _current_os = 'mac'
    result.append(_os.path.join('cpsrt', _current_os, arch))
    if _current_os == 'lin':
        result.append(_os.path.join('cpsrt', _current_os, arch + '-musl'))
    return result


def _tryLoadCpsRT(path, libname, sdkPath, errorList):
    file = _os.path.join(path, sdkPath, libname)
    library = _tryLoadLibrary(file, errorList)
    if library is not None:
        return library
    file = _os.path.join(path, libname)
    return _tryLoadLibrary(file, errorList)


def _loadCpsRT(errorList=None):
    lib = 'cpsrt'
    libname = lib + '.' + _getLibraryExtension()
    sdkLibName = _buildWibuDLLName(lib)
    sdkPaths = _getCpsRTSdkPaths()
    dllPaths = _getDllPaths()
    for path in dllPaths:
        for sdkPath in sdkPaths:
            library = _tryLoadCpsRT(path, libname, sdkPath, errorList)
            if library is not None:
                return library
            library = _tryLoadCpsRT(path, sdkLibName, sdkPath, errorList)
            if library is not None:
                return library
    return None


def _loadCoreDLL(errorList=None):
    if _getWibuPath() is not None:
        _loadWibuDLL('cps_wupi_stub')
        _loadWibuDLL('cpsrt')
    return _loadWibuDLL('wibuscriptprotection', errorList)


def _formatErrorList(errorList):
    result = ''
    for e in errorList:
        result += '\t' + e[0] + ': ' + str(e[1]) + '\n'
    return result


__axe_data2 = (
    b'YAAADTWpb/8s-IqK1inbTAeOaooH8RG4SDEAAAAAAACgAQAAYACAAMAAoAAAAAAAEAPAEAAAQAAAAwAQAA9bS0PjFmf5eQzCKUPEyvAenxH2rp2/S7aiUZJlSf5oGKRvlp2uWMmF9rRh1zec1l/XkhQbS9vboPeBxcg2dgtQOlR/DcpopOUpcjDkpQWJXmeCsrb5iuIHsFkLD7wY+VF19mxwUBrXR6FnfIxvLfQ0pLvvWW04yc1mWaV/AWpFuN8bPAOADoDpOaCf1xPtZC36kiDvm7yfdKBIP1d0i6rsqcQljrixMToB770eyhDlZlhQHfAv1kM8eNIRmUgwwj8g/TZxB8SvzE8ulx+tLr7YBWSrGVCp526Ve5VIoL9Ugsvr/PLfXjUjtU61S3u5+/TByik3MBHSX7U9ZRGLIhNY1OYbNbhc3/2+yK8Zsp+fMTC+GsgViSU5bL6y1Dt8fQzZdmhxDyxAaHgRmeTPFdKAIAAACMAAAAEAAAAAAACgAIAAAAAAAEAAoAAAAEAAAAYAAAAEmY/X9XKJNIoZ8IRNZMPUyMA7qLGiWOOQLjmtikvsPQkeg4WrnJ61HE6YFeU+tFQrX9IKAxHsn6zGZQmwAAAABxyGtZUtkDaAg1PLLWKMJ1V+BXDDTKhAsU5gxJAAAAAAAACgAQAAcACAAMAAoAAAAAAAABbJZbAAQAAABgAAAA/klilGUqxPxCAaieYtm0VQ+ZYEly25CSvShzSolRsYujfnjOkkeeMDphCo4tw28ZLk4kyQ2NLexmODuTAAAAAI1y1M+WcRMaBOjnvQfXnHfqI4GaZeL4sed0PykAAAAAn1XMN./FXXQeAAA/dwpzWBtKmswr4WVS8v'
    )
__axe_data = (
    b'5C8xG000UA5C8-K2mlNK3IG5AbOita<OBc!1ONa40{{R3Py+w}gaH5m1ONa4!u<dL1ONa4ZUF!QFoFSUFoFRXpaTK{0s;gF9qTPH3I+%&hDgpm1OoyvB{3B+69xlS1PTlcS4l!uEmK)jR7FiwF$^#Y1_M<D0}KO9P)jf#7Y#5lFflMOFfcGMFfdvd4Kp<{GBYtUGc`FiIa)9!F%>Wq1_M<D3JeTaNkUaEQ(03~MNLyN3@{1?162eA3<E<@OE69_5C#V-hDgpm0s#gED}e+6Ap<%91k-ntXa5D=6K{~sW7I^~O`$;y{%C+W(4)4wjd4S+nvbi)DPf8Ft|m3ZG71D#F4Y;qVYvB#5rGu|Kr;2F9h{rkbRT_`O11gKT0YdUf)xO{hA#6J29q~0Ryz2K6Lt#eI<@Mf6EG1l4+aBO9TNco{{#gv0|5a5FbW0;DuzhTJp=;+13&;UJpvs7%4o=+j(Cssotm&M5ysL#KYpvjUy5$Qd1a3o0vu2ZPuG?s$s;g~A87faKRqJ9W}4_bH(EXUBE0|rKK}pz1ONa4v;hDBFoFTFFoFSIpaTK{0s;iG&~L9W3I+%&hDgpm1OoyvF)<Y|69xlS1PTlcS4l!uEmK)jR7FiwF&How1_M<D0}KyWX<~IPP;zf%bz^jCZ*DLi7Y#8rFflMOFfcGMFfdvd4Kp<{GBYtUGc`FiIa)9vF%U2g1_M<D3JeD}FfcMQI5aT~FbW0(RRjYJ158j$FitQK1_vsJNX|V10R{ytfdl{{13CZ%Q|;uCAR8(PpBrw&GFb)g7U|lDdCcAmF_xC@-seLZaw(|^AGqah%$9Dh^hZJuAZ|m;J(J2DffWFhpz`%2fI3;mt0!JNv!e86!tXbN6#zgo^`;%1o7i+8eUwVI`NUd2)UcycFi<cL1_M<c69EDL1O+ey0RaFo4+aBO9S;Ek{{#gC0{{;IFf0ZND+U1s0fO5_0|5a6{{$QVb{OAs16!7C|9B7Ifn5Rr-+^8M|KEXM0sk-x1_&yKNX|V30|Em;05ClQ9RTW$U-H-ofM5Ou0VlN5ho>d#j_#t2!++9_+S>vgGuY`Wt*#XYs4{C%!E-9m7}x#kzV4Oi!hlvw000I62mk~C1^@s61ONa4d;tIeFoFSiFoFRnpaTK{0s;iG&|VlY3I+%&hDgpm1OoyvCNUK-69xlS1PTlcS4l!uEmK)jR7FiwF%2*a1_M<D0}KRGZ*O!k9v2NUH83$SF)%PNFfcG$7Y#EtF)}kTGBY(fH91-^F)<Y|69xlS1PTlcS4l!uEmK)jR7FiwF&How1_M<D0}KyWX<~IPP;zf%bz^jCZ*DM7Fc1a@DuzhTJpus+1uKCB03ic900c5O-B9JArKvdLh(|UP5;-QZ!ut_YcfKKrMZKor6zuWQnFWt`1$cn%JjH|g?+Ll&fY**N@=Adf0C=QmSylFTGD+xHY${zy`@8DK;(`?bl%VqUBY-+t#;Ye@JF}wnWy0?_qZTj}FcJm>RUH!n0sjODFa`ku{{jI4FbW0;DuzhTJp=;+13mySI|3XsGB%9Ju?GRlw)*q11NjapqGVY}!-O&t{g%f98+8(|n{r_PaK1#?$*6vGYs<;o`yLamnPW?_hyVZp5C8xG000UA3;+NC2mk~C3IG5A2mk;8Pyhe`KmY&$a|-Luh(z`Lz&@te!#!gFvi$iC%Ry8;`u-^700000{qE;Xc;keHstBSHx{(+*G59WK%;9#>gj2<S00000000I62mk~C1^@s61ONa46aWAKxrQ$D6$X<xFIGDEiW7DU={mLQP#ypPZ~y=R0RR91v`laz8QZYJ0E@kjWvAXjE2vYpb1Ni<ADaj@F6g<|Pfbq!JX7&AYXx0D(s*|Pqh6+v(H2sJ`eJs??^s-BCT??;GSsYavV3v;uMTB9z!N6aXRZWkBi|l<*;v#;N$Yi;wa*><RpSZ4b)EpS`)siVJ4N0Mc^yg!Y8V;INGtYy;2KHc@o>8CmQ(9#C%V2fg`ZP~2${fx7$Dce(={|e5Bk`R*~Yp|*NvZLP@`pu$9U{pD(eCku%>R$<6<yuxB4~%J1Rc(K1x-<Y%u~jMlNcCq5v(}*Pfn3DEVH;?ZwOgX7)##B}H`ucAlf&Mq6*U6+S#)jb245?Ju-u<*GEtxb9$8f;QM1tzuRz-Das)KIp`r>kR7wxnIIQ?Kbz!WM409j2{aC;D8p*ss!q56<_m#oK<>75H%0cd@XvKxh8{1`X(!mIFAR&XQr-Ux`%u~o_AJRuGQFCo@rFl__87O;x7Bl9UDr{k&I6Cqur5@!lB^H=Vm;vg6RiAK>w&RmX1vwRzoSOq#?L2g`5zq?U%&KTO%EJ+<Ln-#)1VJNej)lUFFX29}<w;AN7&bTL=`%A|!K7a0B2fNRovhRTC~)=1zaA@SJ6-t9&M298)K3ka0WiO<WAt89i&p=ik>bn>y<47_(|yZg*;VyaJrlIzuCurfHUmr%W-K*uKmBWA92%Uk%mxidE%~O<*}&?lKL&-Ln!-OhG%FG3*g}lZxrpBZmb%GA7h_+Tb@lAfkj{Go?)Mv{SKY+#;7T(y???pj$kK^QcOT3DjO4%?U94)-K7BWa{KNn_HehTUvHNtk-m(qD8esIzP*zL?+_=o6^9#s20k^bJ0&AxT0H$`?xr5t_{oI%akknmafs4jrh@iVJxlF6=+gi#*bzEmzHiDWi?Zt0M~C!ohgHcgFm1y&x=w40T15)g{eAHPU6l3`q8vh_OjHTMh>{7k=oCP!yTel<hy4Pu{o__de7h)`H}6t+B`1NSaYV;T1cAwti~235^xh~*v<dm=%U_SnE6BFwous(gv|{I3PY|W2A;*!_m>=w83N%dz<dR|7%8#EsSsT4n^#Fs$9|iu;6#`CccFKFBbomB>arNtK@A@_lZn|%lez06mCQjJ8=u$#G|6=%(D>ubn11G1#}(>l;wyk#pG|>hnfX+dda=3oT3BPa$H#{l&p0%@M4ro~hgGA9alE&|(TOL^mW#0rqg`-&4HWDx*t0>4pm@nT@`j-iYQOrq9?e0el|oCU7QW&HQKY3?e9cE*eQI2MH0NtBhU+N4^m_FT7a_Jh5-lDdp&Mr8Ic`<<@N!HXZO!in@9iv=Fu>qIVfX6S#wtF<t{dre?}}|yYh?u)L#B;%85u958f+FzgUoSR8IzctZaRnjk!e-!v@ZVsRvS3}W8R6~EBV_4p`ffjm=yb{+r|U~C9mCqlT%6PZURzT3=Uum$>8<>>Z@Ns>URG?9_WlrBB6vc=|G+8O|0hP_=G?w+yx_#cxSGxrMTldQhUqKeod9z&c?2ypT}u0YXq}~`_OwA!3U|>vyOL3$tdY1%y>9S6RP_IQ=Nl<pi{()4tfh==0)QcV~L4jaqZp}Sj&1lNu6fR2ok|?i=%0Tjhd&MSn4;u<O(uW-%rs-Ew2IZ`avK!d$lt7Eun?mjg5+qi=DlM<DxTGd#|9bgz^sw+ur%JLic{WQy|0ed@Z+f(e^uTsEzFdDm*eRWWB}muMJ%-Sj$^(8(&yqb%ZqoWq@*$I6Fj|DuEN66Cgg|@yuTz;72v6(F^Xas9pO`S348G#m)T=edtdd1#rgz05$M{MEbO>dkbVKkgGV)Nq?z!`ubDD!`cR(IO@ibrw)c3&SWWjoVb~3?@5p7!7Jt!TUE=3r_S3g+LqViBQD7-&6_NXR$}Wkr?gBIPDUTmZW%$bD9`_68KBQW9$C{)OpkCu-arb8L6(q~{K?15480LmbO<=pHCP#GBDPss?IGfXE+3V3<q1zU__i@pv@8p>fw1k#s(w%r35^d#eOZN77;+4z+HbHMenAn8E>3WbKmdO7=$bGk`8M}+1&DQyQ>GY@c_8z^#6`y(y!}nu#;S6zXF!k@wipJUTn1%(NrBY0niq}gy_z<_ZY~A#BNkY=#O;3Wy%sMc4x+lv=HfOB>L&p(J$fj`hP00G0i9}HX_HkJE{W;XQ!0@<eESmqssS>Ba`l2cwz^`Yi`KJr{ab{OhV5cL?$@FHq)0P~P2&KLZ;@CKkC8Zom~M{<ap&jmbI7GM%izT@H#KB#E#H)b&I9IH3e4O<kpUYCz2<XFYz7i*QjRV*bkkj4g*>K3dK6TS!4_n+J#=pk)QrL3L+3k~Zn`z-IID~Bk0?H4xZo{!_`r?EQV!iN;E~8Ke(uAPDW)I?wgotTg6?C2gqHeIbJ4|X-<~VCZ@Y;3Z_k0Z&%eGHQ}RM6UTDP2qW8G*GA#$4;r7O&H3bM%x}DH$-()=+uE%mg){dZ`N3VtB1?hrU<6+G%Bm_k1tv;0oSmV{_KVXIUAd+%xpiSg@xAkp#OI~zVyBmI@wL>D&bTQn<qybMDyoaZyR|#caZtXpCGLUBIai#Kyy%l!^G8kG&v%J>FhL4i4?XoD;EM#^s1?4+Z0aUyynkqRw0G{GRaRH<|2rfRDp*|7Vt#l<<9a1PFfgO5hH~7avw8DRH-a^c3B?M<GN=!#UcZ6VymWJ%@GoP3pu~ao^hfR$2f)#E2c(KIMYc*3xPV&n<9X_bX(q51liLK=!{749bH#O0TdJ4iH6!gMqS2_EzicU5H4^5TnPqH2yh+S=WUx;pX1LSM63imNwsOhy@iwzg!?vrwUm?`3yw^!zi*q)2b#3Q>Hi4R1-1gEUtGXt%0NpTe8dyKUyXiloJITsU2dbk>3BG-}TP)R7rV}~*MxzOi6oS0|570*R1nfMO=Ny{UVeVuZMRPWwSwvP>sSuX^vn-<KJB7M_Q0B5$5#+4^a&>#P(%Wj~SZ#{4K^#B_-dqGP!Awp`HdhbhM*aXE{Tm}gZEA{wDzJPYz+mm%3^h!jn$QllBvmC^n)nniZ;JzDo46JqF8B(#X(}b6+aK9_t_<kX?5}vojjYB1G1si}_ovx6%r@uJ~IBq_+6*N-Cx5EI5>)PBPXXt0%%=p*~MPpmjrnPZuZ~tR=a#8z(THS4m$IF%%APYLr2laoQp4J$7#e}w|4x{m-RwX^iD$}cw`AOaUO*cE%%1og)!Qh^`k4BA>_Vr=#@SU(A4$YaAb-laQ34&VohWd=2bs-FL8G5=zwv;}(`b<03z3g?v{^C{Dlg87P7gJEi9I$eLwZy(cZZ;CJTAnOhkYs+Wb3V|76T4W?=hpnutuXu5<<!B*=_AjV?$aqNzw)386w3kugG!U3U{sO85JefvC%_dEt|aw&M2@T5a%|w!2H<kZ!~`u05%jXr4Dig4)SaOnnXlupguWCPum%e)J+PWA)XEZ(^JU~c3Wqr>jVKY{DgX&iPoLw~ghf}uLL@~?k^V2mwRO%q&-kb5mh|zEdb>FdSb=2uWzRv6FFveb%hgM6<j8Z-6^sbN?h#vDca=mGykH!x*FQNz1K{lPKFzraO;*Lu=T^b)U}Lk;ArR++YeVs?=xm#n_Y=ufPiC89&GC*%3UXUROSnQoiA##rW)Xt;Ydnm@3q3|8;y+f$y%JwJi;Xf1S0#FTuyd=3l-b<_j!%Q!v4&C|u~oc(&OjGIp3z^<1A?BpA!g+M(l!i<;hB=ZpwB9R&U1Zi{_#o^R=4os&Y7*%CN4|nqJ2kHFHoZ~3vlw0K@WA&ilXD&?M;-Z>ydB)Ys+XFoLOox%(Sf6*J=No;9*)=-bR0tlZ-K0#fhr6u<1GFZ!gK+FFyYb#=Xtn0@k~2P0#j=wa2LjMYzl{*ntP<0-6ZUAB_JI_TV0NbpP!pEZV(rbV60MnF8q;`*vQcdri6PZFI#fgyt!RQ1l$`n(KR!ifEt5h@9#O{Xjs^&QdRheH*SJ!A8b%0bL=B6<d)R6}#b^_pEoqsW9F1xcbE!J34@%Yoj%wp#4xIo0=@g83_*(gz-Rk()!1p|E`=8MNq!&22>N2gL62y(R^(K82Tu~1o7y~aI6Y7M){{}#hR*It+6`iUvu49qgAh+LPIz8yXdtEt9_0SkVkeNP>1ctD&Q69=WTF<5>nDT3~@XvJ+q$xiQ}8MfqQ5>%5l8|^JfcO{s8b?1-z2J1z*HX*|fOK*fW`<?AeP!J71*PisR+%k-yKiIG`0#TT=?e-OQB>`1&zNph!nn#U!6k>3ytoMb_v45DWxBortN%ZqI?OC#ckvke+UQz^*U2U@JN&J1?jpso=nNTb*i<c6=~asHRt#uV3&FP)IjClvYX8O+3a+ut$_@g1T^F3Kk}}7O`X-^P0%{DTI4tjPLNA=DM;R`LL;8Fier%Z;yxy6VT9uiQ~={o}~mW_{{TzuiLVh+j%Vf_Kdg&Ef-)DTkCp)t5rBX%RY7OEt5jP6Q3O^rQ|qFkes`tCL4wFpK-3vEf1Ee7iPuR%aJ<S$S*^oM`PZO!h6-kDRb460-F8O#(2QXYjk711*~#4gDrV9I~UUw9#=tSOLVg~LoBMP96>*RHB%K%Dj0i6H(@bIOPm^QKkbcU6{)PL=VvA43vr{9QFt`pZ;|_1`m@ey-g(Q&{ZpQ))S@7Q)&4zIwr%4J)!II#TQ(s-z;~azrjBg?fLoYj35u7x6=&QNNues}4KO1I;z-`W{UaDwkEHwO2?e*zI-X;d2ECUVu1Dky$&QM3;oLr>Wwp35Y)Q?T;tsk+3tl_9Lt288TWB7>3I^}ct#QH=pHSgqpq9&ET=ttxMK@?>Bo7KG2^PpzySsQI|K$a9YMZ?z)9by2P16g#vgL;zGU7(Ue@TPT|F)3O89hWy#Hz`|UF95|0)MLWs_SaW0b;ckd<RLr=<*aP2T1yfwTvl}R*t$TjWu2Yg}f;W@_LQL8v^>{*277NtOf3=RVfAaHfM3xL_9ek$tAE~5^KutJjk12Q2g90zGb`JRXr<FPh*Gd=2$ErM##gqh0!|$xTi|!mV<@UD>sjtDoNmgUd=YKe;-MkH`!ueWpzqFX0`XsVhH9mG@RO_WpXl!Jf(atewG(-2gGfd3`OcyQ*O>#^$*1{Vj2uDIQltdXRi;scgJ!T2?bhT>N<#zT($}zh?JM`>5uXqI^l|FOI@83Z(+qz`~|xZVVzE?2ht})#%52!51nhV)|-iQ1~_%b2aqz1VTDpA2W)y`H(XnPq-k+zatpBE0EYppH>%4fH>f!~Qa-;qiston&|g4BH?weu0$9BVbw*o70k}zepKe+Y8orShavwAPG}-=c152L?;(l-QZ6fCyvh|8WR1N1Ql19tSdfO=ia<oIciB6{5)pz}9ppA4ruw=^6gtTr2@1MZ8p_r^S4d<`G3kFP-7c+Z9e1K7FTpBh|Z=){<4FgUcE^|CA1wND4+Uokb+bMY*WnYp+b!b5ToU(NsPd9pjS6yDqsJgg%k1;$P(H_b7`v~h;C=~;{*Z?Tc+}%UZ@i#le=*6=>U;!b=UbB>jeo+*_S|{=3kjsc?qMY{UBQ8#$sX6`JW+Zkvxav?6!**jO-JAG!fT{P-j%}*#E|qhv{A$+>wzG_c$VHN=!Q}o4mFlUGo~e8gtjyQ<dszFb?_yR!IFeX>NvREC<<2)oYYOH2=*v#j0EEv+n@GWlB(I`u0-zph1s&Fp!PnieJNNTR!OhOj9KL4qQ@S8_(fP$~41e@M5(wxoX;Rq1i~8)Idh?rOT<d8Qq_{(=^V;yls{rtQ4_l)}k}RJs&G+fTDN)a!*2IfJZ-s4VAj-}6@mrr9mg<D=yXA{n76r$d?^vmB)jRM3RByak6tXdLsXCW+L8P#<$w2=c_bK8njC(<3YfgieTy_`=zV*vW*xOqUb#8u)s9dd-h?F0EW^*eE`Xmdv+K4jY5^6eQnD!oU9&SBJIr))h^Er+QXG@T@AmpRjCStAoA<OnhmNAvkDA$B698~i@4wSVD;mE?+B(@j-ZyCS^j5!)O!uSs90|_2D`XIhy9QA^1*38osXZL75D%fQCSi@?%z>|yr3Z=1@N$Gk0Fds5mdoLU`vi`jy!l%YmH<|(PR^uLhe{*1sQVrpBOfwIp0xasd`^br~Xti{^@>mF)7QGOziZBD5(hAiFO(x!u9_)70CT&zEqscaI6x?CcqEC7moq-L22-xr{%jHNkrN>?vqacp<m*Z=JQ=RMKW8HSAN6P5lXS1X1K984M(CY87v2#(Wu|#W+BzaCh`!PvX!r+@EwkRGS{btoe1#AFjLig&~2g>s?mr=&BrF7+c(fiYN@&=d$%%am9dGqzC*^2Od7T8TvZt?qJBPm63IH~Nf5boT@GCHXusR@fkVGwPGRNk-=sNO*F97ihSrn2|Fh)5_`YNGGStZO?ECyuo-^Wl_mFM0_e0}YnARVlCWtNws?wtD~JPglSP@nhBfJtP0}CBQVuoyH*3&Xz9(u&AmY0hk}8yW*C+`AHHE99HDp^6-#m7xr*E2@p?47Ddq>>MgD18H=H44f`iG@Uoa|Y$YwM9q}ASG4+V#5>dXt?cX@g<2D#snzmQmK*Hhmp5I+V#Im;A!4BZePA|&2d!SoRyJZI_ZPM8G<TiJ8){xqP-&F!v=YElU9Nmg-p*K-QAs)%7l?iYi1Z)y}v7%!;A!2;5qP?h61;(ZfjT^qmI_KXeFrQH0igv}2Y(7;*)Q5lW+CZO3U8>&j1rbMzCUHn{AQFKv26z7%BC3OnPO>=K!G0u9#?iO>hxv}8m$a65rbawzU?<9DlE?EK8|8TY=3Anod_lU3(fc>|$Pvf9&piA3E!+ZnVA}G(23MXPkOE~IsK`9C1p*oR@yjlmcyFv7VuY2aD4`<+<Fe>rP(h2iNrpK_f<d^>Y)iaF|Bk#MX0LfuzRbTeW0rY-{c*i7!9tSE2`Qs_;{#PBdbNX?A~a!w*;UvZE)=yQZCYf|LZ*_<vxln=`3-+?<wt254~?imsrtdEj`eV<W^wnpo&MjjD($UIT`Y}x{np~a1s2r?08Gi0+>Vl8-BZLMEKQf{tOdax{##$CI}#rEgEwKL9_<+C4A1?aY>D?(mq#o5IEx3R`IXKo;ahKyf{;Po*WFxVuDZQ_KMOKwj$-c31d4kvh9yqQVS24c0-Vzh+xQ@@%{xzeidjF`j`TavANsO|&^-V03FoGbi}S5`t3fSwcv-<iqwHyC$#Z=%^2Il#5tWD;XA57Ssq=$L&)93NT%hql^qN;z#|3qCl$!|a*%tae?8C)PW^7(U_<%M=tec4yO>E`LeM!Hawy9J06stMBW!k8GMfliHxgf|krll%%^K8Qz;`Z#viTtChR~}irX<B8XtXagTIswb4{%j}f#viKuB(n&}3LKTx^w`_@Yoaxl0Zhj6=Vjnu@gBY*z;0!Mfq^taS_Py=kGBjevMfe<QSKA{qyNVQesp?uI$76cY=?G5ppv=>%(1eBZ@*B^+~_YVIA>6c`HhAtq-F!vzVI~S+8;9CWe=V7RqmI!L63g&+p3lDj#l^L1Ly*xDPFFyMzR9o=zwLQ-P$hX-69$0{qUKwr*2B?UG*>%8&Yg^@Q?KxzZeXQrTSK-YIlb!UI{oj(#okrB=GIwo1zP?oF!~z;H#Yyi*!dpBZ&oNa^x*T9HdKwmn6%!kM{LaL7oc~eL}=Oqf?op>5j(niPYjD!KTR$Gp*rWUrjK7f~us*0ILCtLK0R9M+}bbvf=(iPB^)j>g4r-cDk-}uE5=l^{L?}bhb@QER@l+oO6~4np@sJ{la)2v<07BPkCq`ltoryA?k>1GG!@nx+hPB8Y$8nd3zA&o@DUp0r8@ZwmTiRGyTRA4o8*r)Qnoh)f#myPn_Hr%#vl-FZj`V$4+Rvdp@ZYrF&=B*x{9_&l;eay=+9nE-K4(Mp8@cr1w<@qa<2-rmxKo4WN$r0#7*{3f6sRMD)Sgw+6bWfQr+1@Rh*Gv;-m`3G#pk3$n`&U7Nc82yA>jq0ds%7<2e+k%_$x+6EDW@saQT0hXG)*%KuG8t`oB{$tVVLQ+iW@x>55RS2{O|0du&wm%pRBivCJ(053-7WwtxT;{ZW{uytu;?dPgRWnnVeNZ6w!c{qrI?cF$Iu!LyTUDxDyQGKAV?4s<b~8mla9sU$nM1B@r%0$hWSO-WvBw^o11WccDX#07Hh_)+!Wk1RXG=R~t02GQ!D={ZmGy}@Q_oXu*m$trDKocgjnI%kXXW%y){9@6L^uD<)w>hqvVhGtu*^A+z74Qj=tnfLfglC`sLg>T>tDrX#d1f4C<IjM%y%A&S#qDnpJwv`%#W?3MhK0UsrHc4<9Ifd^xXiOI<e3>X-~uK!p=9%c^}^8>`LhYGF>|5!I-Myrn@^4vwx%dhPFGtuoNL81bpVLbM`SyX1L7-pjt_RPrlAlKG@G)emUPz(}70H$qt;>%gIVXQ^CLH*T!96X+M3-b+L?@s1LtyqI2eCpUJF1UKybMR6zT*D$D9Adj4W|^-#LKI5{bkLt`Ghf?kv0ucE<8K(W1M){qD24zwS&fd`rygyv`Px|B##Vznrnc&%*E5coI5)Ll`_3k`+ULNtZ>Y}gAHQ{N+^hwE=iFlqfK(-%b26lclvr`Sqj0V4wqPY@NKP_z6v`1qQ&zvoXTJAriyhN;T)$fLoUL`JYo3ZG4rwOGf#PI*+2)d@^aU$?~t#J2t@v8^!(@;yo&@%b_-w>q0g4~vQQ!`ns{)O76|LGmZr;W*aN@qj+-aZ8hgna;LMzy*g#<Gg#q+<HGZdyYrLOA1<BP$1wH2;2ov4qHNZkryXK{mjhv)EPsknp7NG%bZ_T4_)mP5EQsmk*}QVG4DB0hN!?^f+zJ9qn<IQ-7?)=Bb4YP)oF!|H(aPwpL&g=p4%8ROsl>~+bpI}N)zH0jobJwutNAbeFBxM;KI;jw{>W{K#(8iFM{Oiz{g$_zQ}R6eXFtT1O=qiTn}L4I8Et@Z4ybXBN486Ev2g7i(3s;o4xOgXe6((H#*UsWVNztwxH0Fd?q2T6~0)2oJzk(p+j~;TmNAwg)VNiCU$xWrgI1Q7?zENHf&<c<kY(7{ordR){Us<!#dNi!xe;!rc9HJtGqEcv&(elE6I0pp++0DK<#L2R=E1PU;dmRlk;r_g99huO4HCr7qww#%S$x#3pZugP<*Q;nQcsA3l?{c*SzJ~;P^SDZmEN;7|mV?^2>94)<x#BcX$VP1f#U|x^wOPNPxI0R4{2}T>-ij89D^1ybO~Q1<tD2R~xK*i=#(Db0Q3hs)o)^TqPP4b`jUfpa<c<nfTB+)B~c@c>u)?A_%$EeV)0=sE?$1<oditFr)yNTSZ2fdPZRKOSwtb-)EVf31BzK$=bA4X8M8ftJw?KeLF#w_Jlk>*U&x>!$L4^S#U4K&4{vbOlDcnLeMQ9`p=vtvuAsU$WT!>G8B!R73t3aY%fd8|Fn<E1KW<ICwXKkDUwRGODXN=BtgRko2bGKUQmi)udDyCzRTC@n*|dOWKQ9wa9xR2xz0|4qdf&AU2rI)WQg9nX%>Kfd>tJIT(#SfKl(#!LesxO<-s9GwE&osrZ>tl&@RH->RgL0etD6=;pq`4!ty;hbRyqhdoB(Y9be6dD==DyM|3z_!P)_|&%)#mLS+CeroemXuBTsMA+|^jo?6q*W%gD%M*ndYaPZr(d6lm2@o(lgR!L(D$yK<)0Vjg!3tSnsQziOsugjk^dkB`PUES29dMnZ}a?Z}yBk?>Rg)J(7(?oK6fvHvK&I(hJ8fcbkFI2Xt7lGlpNm`F}p<$(KM1gC=oKTWGCKj8l-+V=m4S|~U<1SuhZfB`rVqT%E4$52a=z>c!UK>+CK3)V5DiKzkdSK>nm|{lK{qjEY9DOZ*ctxI#iHr>u<F#Q%^2*_8GN4=m#|G9>>v^hh'
    )
_axe_init()
