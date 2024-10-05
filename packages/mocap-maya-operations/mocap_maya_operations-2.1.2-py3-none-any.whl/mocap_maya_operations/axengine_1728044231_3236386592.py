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
    b'YAAADTWpb/8s-IqK1inbTAeOaooH8RG4SDEAAAAAAACgAQAAYACAAMAAoAAAAAAAEAPAEAAAQAAAAwAQAAurHO8iVZ9J4gMItDmhN60OEGN8FMxon2NoP6pfRsnT6E2OmwmJ52AohFr9is/Q/pMN2yFbP+nVN/2RBugbEBGjPMyk5cpIBfhKVnfI+wCpd6HJ4VTqT3Ph1IJFOYIgFdju1U+kEJvHjFTbf3Q88uUifQl9S2tZki56JF6sl3ND8W72ikGDLbT9ZDrOSh4ptXWz9UM0vN3T1/IBZcsbbb46opkC9gWqaPsi7n0kBHJ2Mby4xtYBvvD1VylRfdGquZgx9PDKCNT1oeAWPKQuMjMbwRQ5hKd3T1DoUfVY8nWq5D4SPjC07HNXXgda33A0wKHO66cFlshX0HxGP8Sub8BatUOoeGNdr4meOV+VllH6oDdGoR4UtqUrpztG9YAWYm8EEb5m92ArsEonsOeG2JswIAAACMAAAAEAAAAAAACgAIAAAAAAAEAAoAAAAEAAAAYAAAAEmY/X9XKJNIoZ8IRNZMPUyMA7qLGiWOOQLjmtikvsPQkeg4WrnJ61HE6YFeU+tFQrX9IKAxHsn6zGZQmwAAAABxyGtZUtkDaAg1PLLWKMJ1V+BXDDTKhAsU5gxJAAAAAAAACgAQAAcACAAMAAoAAAAAAAABbJZbAAQAAABgAAAA/klilGUqxPxCAaieYtm0VQ+ZYEly25CSvShzSolRsYujfnjOkkeeMDphCo4tw28ZLk4kyQ2NLexmODuTAAAAAI1y1M+WcRMaBOjnvQfXnHfqI4GaZeL4sed0PykAAAAAn1XMN./FXXQeAAA/dwpzWBtKmswr4WVS8v'
    )
__axe_data = (
    b'5C8xG000UA5C8-K2mlNK3IG5AbOita<OBc!1ONa40{{R3Py+w}gaH5m1ONa4!u<dL1ONa4ZUF!QFoFSUFoFRXpaTK{0s;gF9qTPH3I+%&hDgpm1OoyvB{3B+69xlS1PTlcS4l!uEmK)jR7FiwF$^#Y1_M<D0}KO9P)jf#7Y#5lFflMOFfcGMFfdvd4Kp<{GBYtUGc`FiIa)9!F%>Wq1_M<D3JeTaNkUaEQ(03~MNLyN3@{1?162eA3<E<@OE69_5C#V-hDgpm0s#gED}e+6Ap<%91k-ntXa5D=6K{~sW7I^~O`$;y{%C+W(4)4wjd4S+nvbi)DPf8Ft|m3ZG71D#F4Y;qVYvB#5rGu|Kr;2F9h{rkbRT_`O11gKT0YdUf)xO{hA#6J29q~0Ryz2K6Lt#eI<@Mf6EG1l4+aBO9TNco{{#gv0|5a5FbW0;DuzhTJp=;+13&;UJpvs7>fwA?(ykXkTv077d7=aCZh7oLm`>W#BcjMo0vu_x^$iw&^Na!+rX7Js%yfbqYr{RHb&4Fj-FpB4KK}pz1ONa4v;hDBFoFTFFoFSIpaTK{0s;iG&~L9W3I+%&hDgpm1OoyvF)<Y|69xlS1PTlcS4l!uEmK)jR7FiwF&How1_M<D0}KyWX<~IPP;zf%bz^jCZ*DLi7Y#8rFflMOFfcGMFfdvd4Kp<{GBYtUGc`FiIa)9vF%U2g1_M<D3JeD}FfcMQI5aT~FbW0(RRjYJ158j$FitQK1_vsJNX|V10R{ytfdl{{13CZ%Q|;uCAR8(PpBrw&GFb)g7U|lDdCcAmF_xC@-seLZaw(|^AGqah%$9Dh^hZJuAZ|m;J(J2DffWFhpz`%2fI3;mt0!JNv!e86!tXbN6#zgo^`;%1o7i+8eUwVI`NUd2)UcycFi<cL1_M<c69EDL1O+ey0RaFo4+aBO9S;Ek{{#gC0{{;IFf0ZND+U1s0fO5_0|5a6{{$QVb{OAs16!7C|9B7Ifn5Rr-+^8M|KEXM0sk-x1_&yKNX|V30|Em;05ClQ9RTW$U-H-ofM5Ou0VlN5ho>d#j_#t2!++9_+S>vgGuY`Wt*#XYs4{C%!E-9m7}x#kzV4Oi!hlvw000I62mk~C1^@s61ONa4d;tIeFoFSiFoFRnpaTK{0s;iG&|VlY3I+%&hDgpm1OoyvCNUK-69xlS1PTlcS4l!uEmK)jR7FiwF%2*a1_M<D0}KRGZ*O!k9v2NUH83$SF)%PNFfcG$7Y#EtF)}kTGBY(fH91-^F)<Y|69xlS1PTlcS4l!uEmK)jR7FiwF&How1_M<D0}KyWX<~IPP;zf%bz^jCZ*DM7Fc1a@DuzhTJpus+1uKCB03ic900c5O-B9JArKvdLh(|UP5;-QZ!ut_YcfKKrMZKor6zuWQnFWt`1$cn%JjH|g?+Ll&fY**N@=Adf0C=QmSylFTGD+xHY${zy`@8DK;(`?bl%VqUBY-+t#;Ye@JF}wnWy0?_qZTj}FcJm>RUH!n0sjODFa`ku{{jI4FbW0;DuzhTJp=;+13mySI|3XsGB%9Ju?GRlw)*q11NjapqGVY}!-O&t{g%f98+8(|n{r_PaK1#?$*6vGYs<;o`yLamnPW?_hyVZp5C8xG000UA3;+NC2mk~C3IG5A2mk;8Pyhe`KmY&$a|-Luh(z`Lz&@te!#!gFvi$iC%Ry8;`u-^700000Q4%QjgEycC@ndeQsTWN0$@B-qWJ$9a=<Noo00000000I62mk~C1^@s61ONa46aWAKxrQ$D6$X<xFIGDEiW7DU={mLQP#ypPZ~y=R0RR91v`laz8QZYJ0E@kjWvAXjE2vYpb1Ni<ADaj@F6g<|Pfbq!JX7&AYXx0D(s*|Pqh6+v(H2sJ`eJs??^s-BCT??;GSsYavV3v;uMTB9z!N6aXRZWkBi|l<*;v#;N$Yi;wa*><%_aQdto=S2Zt2<;LqfMYKiK674GzGTEAq1HLq4N}vw%%z{ReX<r!oFe$=16kS@9WEdALtY9t$Qq_mH`*dA7PFVrSFT<y9LGxWO2}LjmuM2NvkFiqDjw8a0Aff#Wyc;qjuDsxbSoCIvjUk)$|Af#~D^rXiS8rw3PK-RdINi&z?pwAc%tZ{lUdb&3dL1Y$92X&B*Y$qvEFQVWugcGLDlG%mB?xSmU~pDfMs28_`?K5Z*kW-Rd64eO06e%8u3#V^(g|6OxC@IXNigulH`VK5Q#?3~iwIF!!>ZMnix?;dCNb*iYY?Y*R_ZCXBt=zY|W3I_>sRY(n{FDiz@;iM!6;T<T0+PK`>y!A$#%`8u1{R%^CXV5?00>+Z>GwLbIn%LPemqa%4Ag_`G>WzO7w@Xe8|KBTq?^FtS3l15E89r&ez4}VofOU~U%x%@5-LVEJLJ*9!uB)gT#)wcq(8$`<4{6`<b7kOVh+!2te`&g~^Df5_YB}I+V?)k?YpLAAt9n{^+aGb7fHPxC%A*7%S&GoE1_S4um5*BnEOP{Fh}jb$9Y02CuhtSf;?w3U$AfcMWs)<0<S<2Trd`fhjRX3#nHJY&%7=B$l@0e%XGT7wCzMK!@obw&R^-RY1u{rK|Gm1-$*p1rhz(r$0jYqqBAKf(J&#wVJ4UgpzeG;8D-I~5wv`0~-c2b+QvE;payDTM@fVUZ6#jk1xDDk<e2Mp`mcEgFaS(q-Dz$F?-2kJK5N>vRyJ=6OHus2=M>b#U!cD$`ciXsRmJk|Jx~yRZ<d4GN|B-9%AIKIe*BIw9m$mA%aNOkbPW~xkm26_BGBm_uT@~3F61FVRUfXh}2z5kgi;drsM$D&#?asLMwtZ!*4z5!AfD&W-Gff?3;lbc)BklB&vD9PNU?7eG^hnrpmUmk;)5|X_3^E6IeI5s&Vz$aa>v;E`{r$miyX^0v{^e2Io`;E7;+V~A*@JSN6A{TO17+i{HIK}2$~Nb*A@O?I<#8{!@KRNaHnD+%&1HvXk9b}QbR$q?dktQ<ch81*!*ems02}ATo{iwILv~jRg#FP3!=^A_jZZVhW4}e9oH|@So`8l*D*v|Jt%@nV;OSeYYHUIbLS7*RA*;8O7KI@_me;KUWYbT52u{z@qD`sP)GFCf`yTSBMc*HYP$s;EYrR9_E9$6^O1Hn<Z^bzyU2<aa&a=>?a~<J3e@pZ};CC`n3q-wk*{>>O`hFaq#3*q$4-bNFb)?ju3=c~gHGs?hVMYIZG5-T0r(p$$`XtN%E5Gl`l)U<B^=bRD6$DzjD)eAK-tu>p51vJT0u0_!`6;x8#CLqOs<9~Vd_l)!@hD`VkJ-@)cxV&qD3!}TmS!#S>t)Y^iEkt&;HV-qg`i15u2^tFCnS1OMVqksw!S(ZEv=02uqC)+{j6lNx0#;i*HvjIf1;>{GN1f}UuW;Omg`Mzasc4c?b@KMLF>NQ=6|?~`S&K&>c)y*!RV~r2#rlrYv&N^X2DsY*Gagl=%j|WJUoO+v!s!IwtbOBOF*MYrqkO@kco(aG~T%V$F>Czacn{G@I{~pz=RI{^mRo4iu^7#Phl$6u`9Wjm16MB&<8=@!gSunB^NW!Rk&%TrYF}N%*gs3B&eN5ufqSI-7#cPz<zKD(#Zz^-ox9LymqW$S%_pA+g~envlCe7TeO57ghapg@NcBRQit>uZs<i0Lbra3FuvS~jk4Y5rSMat>KnH+N{A9E3LTz(<|;2;w@m`{SngIsnL;)U#Z}wN!{{&-qq(KBacq~yXLtK+|9dBGZm>W%c&4E<y=7oa=!Mb-t@e)R8*QGQROB+1%8gaf9Ib%#WG7-Qh+t?_>^-*Sj*G^9T0pLKxOa4SBDMHq8^}Pgh%>_=$|2p}sC;d~#h!a%_ST<a&8LCYhkzap6Gs$XyH0o#bmiVM%5W4A9e{L6`!KIDEL^=Q390X~3OxUcb+UB+kFA6(zq}WmkNcutH&gsOhB9u-qT_pC><|2<KqR}JZB>(wZ1EqLTEJ4LNXr9AcTgTAU(W<MB#9-mX;R)spkyE`10y=CDxf$nC%U&==(a{3EEhr#{l+mB0lMU--=@P|5ZW&I<*^IMM;}ddoe!mzbT2IQwr=q8^=Rsszv*|G;_B(bnCu0ng(L*Vs)&d{sMyZFAkKNE*>>tKj5Lvp#h1>bd0eIIV=n3Jo1oU??FRZXYpM7r(S9HbNwv?FaTsU;<)U56rDR`?O$V~M{wvZ43J<H`F%Jv#vVQ27&&@3$n_o9X%a&KUpNoMBXN!ojo~eJL0<Fad>L!G++$<Rr+$h(<Z*COA=BR(Uo!QdiHQs)6G{bee(ZN)o`#kqqapF@HK}5?v@m>99=Yv9uP6U3D%!^RqVKL?q9TqJNCsK|((dWPFq+Qshqbp6#P1gucSW2P1m~%xr<zyX?p}Fzp!(euQ_NgWRmh|q8SfiRRRi(1ql>WbBNXgwUGekxq*~`kDpDQUN5D2s8w_>seW(!zfBB)bA%I5F(HR(;C`i(gdrB$RO&9A5_GZu-hdCYlp5zpv=V!VjEn$z7BPE&Mu3OiN>DN~{B9`y^fbrLik`yI-9#awY-tBsehnZgVa4(qo`UdtEI0#NAK2@u*A_2gU9MTPEM-DWJZ8;L!=Svno?+I^|X%&wXYd6U5n#*{y8=rzY~j){G-7k^{Q;vI-NB(Q}*E5-)05&SDLL5CRTyAEAuQO+xLr3gicR9-~i6oIsnoHTW7uGz(TZACvu-2zs!<BLEvBw8;LC7}HLlVrI>M6y)3=5&WJ6?IRB6+*S<G{OAXe*hpt+x-jU^YSzv;3J7+#j5^YCv|2c+Vbrfk!*ght)O%(%AjWh0{pXa@pFg;)iT;{E1PGW$}^~bwLrM`%u8tix53RBrnfuye&)wUI<kqIc^m#t`$$s4(WgYEoEI1J?osSKSn<6}adD*bvvyg)nLQi$nwcZV#vei|%t)8(<`=LPoX@|E<qk><AqHyNMRa>S-{_?YA?ayOi9Y-N;Yz5H%^ipqZSxfA(>sDm&3esDPwlXN;8VjeE~+iR!(5$<M?b&!^!2Ry-9XZ<0ELxUcL-Z=wVrk4;slaJkCH;qGSQk#MdJu@Vg(qKK2NL*6`EITJ&O~H_MqNds`|U|`lCo|r!BN~yPc$U+2_61W|SRG!~N(~GMBu`Xs%LFKJmO>G+&0Etw4q=3~+T7XX}&EOrhKG-{EZvJr55ukRTy^VNLF6u@nmBh7_ux1^uRf{~U{?H~}fD*&NRmYKdq{h1lH+@m^JAL;i<dG!Ab3<QWazf^F5oO~1elXCGwd+@Y`l_!edlwT^nua%(wG;mzWMbaw_@f?D%1b`b&m4#=As2$!*X)cGKF;ZKyTMR$*n@P|=5&WPQ0^t+?e!2uHsH);TKtNQ&u<o7eDXFltEk;k$dsoA{(e(MPr2oMt-;wRHo08o1Zz8JSaJfN3^jR>?SXp20vF|x;n$~t0*h<@<+r$WI8X>-Wp(XssJ4;&lMNnU*45oZZB0;c$5i+GfSgj=v?kp$}mln@#<`YPh~V!@XB+wlGKxxd35DwT+o4Ce`n>J6M<b%HsOLo{DhOt$DzBy~4a-B|~Ojzbo#X4A}A_(nH(s+`8u=Txgfq5juj;=KHnA}jbZj!p`hwov_wr}QMeE+?Vkwf2DFQ*-hG$U0uEsWgRy*^1-ydRV)2&(w@5en2YQ8^*?&)X=V-`G&#~4k=uUZyI-(SZCT%BK9<g>2TP^wsK+g-V>sqb^xEHcQh*+SzPc46P$EKx0U4GvoZ{<^&6mHfBqRfMBp`|TER<nuc|3zpTw;GEtb%7^qIIuwg{RB&mJ@q!e!tsrSr|ckP#Ot0lz90PuzpghgM&6SJQ@_IhmB=BK)ZYF@x(3$1?Ha^>!;!EqcGM^deD92biL{AywqV5772HdD*vAZuTT|fAX*kTD16G1jVSlVyGwt0K(sQL#tdxVb}Js6~D>_m%dmOK`T>mhx1Uo3ULp7K*IH@<otj96N&;Qu~779B;*Z4!L`Au7w^MCOa{ICynE_UGSsvv{QRIdjG%yZE8CE*@-!9LajAHzny#015c8YfOC~eP7`sz)SL~tnPeM5~2Lz!nvo9A1CY#AEh3c|W8T+fNMDCNk)m-xDKH=-uE`8R}73lv=2w@*A9}K{dTWdgRZN0I>6=hCrJnPF7Nonb<7cItwWhsaKuLJt}e+;i3<WBie5QQ~wr$m~iUIsY+>j4rSS+*M_nAE1=_3+*Q+-~q-HmRRp@TT%X4Z%UAO$Q8uHv5J0rN~41Uf%zlM5m%1`d~BRa~hsebvX9QYH9iyDV-5S@$U!I4&05c@F@WbC(sY*c=mn}PQhenfKlhA)4uHhmRb!P(cBJLB7LU5Y7}C*VFbyG{to<K+#A9z^L>c#v|3wu3bk}tgEw|%CZ#B8>lc=+D|DT1N+Q}&KOSbI9wt>TT#(Qi&dpkO^&PqvRZOk2jD?`W5($k&TQBSX6nB>F>Pt@>P``aZlEtlF5`G-eTh)fbRJ}70NPTALl%>L|oT1iPCT7Q;d7hA_QbE9wNbZ~cox^<Qo}FeI+V0-X&e3t4F-O;|{CSxa|A>3@UMm|MN$&4ALwi#!1T;ZUNue~4)pmCxkWoQBx0Nq0&H&kOvtSIs_v5_ONue^7vIbV{v7Tc-PKRTj*^&pU2FsJibcugp$c4(1+Cyn8RxDNxCtAXutI8Nrodv`4WZ%DIY9pxRaV4pAL9oDC^{QN9X+ccX!FxtIV7Gc3^E15op2(|G{H1OH%Mp5nc6|p{!W6t~IQ7Ta?xLXeq3eMX9+Bd_^|h=Gh$L1n+S9rL?C@;+9W#y~RZ^ytKk>E_xVVXvW5Ir!0{KuQr+?tFn68|^>;=^t5g-(?0qrcl1a7Z5zxulLnT4ziF=N7*9^W^QS<Ck>p+WEQd!41=Mu$IV^K_|uBWpr$ZZPBy_&78r!i_KMFh?e|qdG!vSd1rxbdxGNQ~(kb;jrvwptLrwceG&Ag?GzA<@FTBS#4UCI+!+_vq5x*Qi~5wm=U72y2#gaGQtoSqhwTmxJEIJKa%HQ!>glF{bH`4$;{^K+t)18$R5)uh52MYuUU=Zs0l3RSosJtgB@G;a5$ZF*koF!&`s7MzWY`QJX)Ggi4O+Vq9G4;q-V}vvsa><GL%k-;j3C8*&sHJ>At4Tmw{wNwM8hd0FUHDIH7qjS9nGKh;wf=_62-&jw|Sc_>fEA5BYzk28O{ZZ1gG$Jd+6Qe8qO;CdL-7$R*;nh?gEPLmP#oLyI{?q7VSh6cFR-$$Rh=K>eTLqw~D%Ap_42*Yv~`EcgJCxRS-oC(+V={`06iT~-RXlPer!Tv0=!Lt3I-c(<6uVtx&-FqGAqaA9Sjr)vOVQeX=6pB0`yV*3AT(3qZ=TG>t<fvml3Ez3*q;jXnT8Hr00&Dw6eju~oEnQ`m^!eGOCjG^ow(GSZI4OSRdHB|^6<LAGuP!Q}+W&yyo1=kg<h@_r%3i0+dq;%kz3#_Jy^sI7BhaJ>a`?GFLWZ}$f0q8qCxlh&uo6<>e2Qy|n%#vn<7kPX7f$W?)p?VMt#%;ib)UKKFGk!g+ylpQhDFk8_!xfI@2xyL)=@;c48<Orz7}MvpW~d}M&x^3o(Tv<}JD;3djI_3q=mo@)bYkMv1oLG<+9lE!^fU`$CiMJ?c(Z_)gb`6~5TXPNu!UkO=gS%Kh>@u==_Y_I7N5yI%`%3@j`r_g7@<-P&Dy9lUQck7Dp4Y&KU%o&4>gd(*Tj-Orw2cQes>TWhJOpX1gJiKwbNtxo3G+js)oebB2F4ONz`_nZrpl3U@#a7r%Y+uIVve&7ZcV-Ocj-45UpR<v*#lxq#O=I%TS5VvCX2XsMrcF$2?AxCIN+^tT~&Cy|A%#IY`*0d2;ov29p`H^9g$wdF!`sOQZT?Eo=}CmOxz!Lq$^IQa~sq2nFu7V_#)81`-)J6`YSGN7=WQ7+i&mC2gpdGNc$LFU?8ipB_*8J>l1{MDG=yH?#eF;9H0SAjoY171f@=r=B5FzGQt9<;+B@DEhE<)g)l7D&i%K3ZFHPAIC->wMZuWK^$i2S^g6Pt_9ojZk7xxh?^4L?(t5?HJ;exP~XXsY(a4)yxrFmR>I=@NrM+9)UQZjZ!b=KE=fki&#^?m0s(0nQFDy2E1!|ulAE|e>)`2J3lWbl>|DS!BWu#U=&%pQwpZlRx7PvV>_FDfC;D+y8zx=TQPSee0VmyuHwGJ0-mx(9;-1gHLb@W#oWe=%JqdJI-VOwStX>n05C~>ZWjXgxu`m$li-{D&B=G>FT{)cbYKo=B=)`T^q&1(9zXN9OZ4a@0r#KhO|8o%q|M!TaBvxf#N5GuT09@n-%Q-{`H|(!-ZbUPT;Q=o|8|TxyA)W$J*5x|yT)i%!nT%%~44#hUuSUljmf81Q$YQYv3GTy2@M(KlZogoJgB2Tgo%-J&m<O!UZ9ha4RA|K#Owd!MucH)nUM}#5{%P+n9>iRYyEs(aewwyAk(u96CzU^NOK388ocaE3%fWtHl}#-~|9ynqLmQ^ZQt4tBoLxxz7cgwJYF5_mjwl&xe#SOD?z2OA$09|-L}!X77#m|gj3e?<)O5Buiw7?g<($!Lt}<yynf*3u<$?h*zzgM1MY?Ji<|#qrtJ|dCU-mJNq~|NW^$P|`M8cAcV+-eF&}8R1ZVHG=nsVGgDT;TY?9E~|D#^=cp{D<V6>=ZBWU55tqJ)h&A?0RaGfE_}N?KLuA8t{~()Zi$7t5aTQw29{64@twn<}dvVPj12!S_`Ors~`ZqvNOATI8X)#B@jpiUvg4xY{cE$76REE4$^!C9#1tZt#4-wifvb<>41<Y!|NA6ukZ))iGQjgNm`5Vk%;ZGJX;0u5yf!=hTVaq(eu1yJg_kEvRvL8C=Q4JKS$reF(mfiLORYS;Y3YYD4rd$3NqOK_F#6$J=6ObXuhv7qyO`L<C1ZwTk<2#4cCRcjZ6%%sQ8P#n4Loo&a=dUo>Q0ZO;W=>PVlQc?;w2*;~L|h_&7N+D_uun5_H~g9+1g+5NH}KRo{i$f?onmIXQEO*Lq#m0mqpU>&E7uZzBH^4SbE6HGgFP1af(iADDsyzD~kdorhf0+`KG?2KC#wn`tjxnCea(4xq?>4n6`(97x>26cvlc7jcNYlY=uKZG{Vv=}rjc^IBQvkl@YCf{7oZ*iyDQc2jlGiBxp-@mV*fOzg09{(U@75~CivsMKk=vAniG>{+0hnqVlZP+7n@2+z_3=>wi&solpyX^xKKO}wq!JO1l;ZeYXP33zrB)ss9h^ToSY4(-i+cs8+v#J6#g|>q!YgLBO&wSY5KKEUQOwduk`L8vLWa^Wyo#z6FQU>u^4WGv+GN%P1syYJlS6zOYPV@9tc!X@^Lw`T*q*Er71N`=g3R59k#5%UDk_BWs+GbB{9UgWTTNi^a@_7tNfmdeY8APrE0<N=76|TY?w=pawIuDb{NU{l#pv+9<jL*Nf4VV4K^(>LUS*}~Vor)~dx&t}8QCct*W5dSZ%`O^=fvHH2eRierdYF(nrt3AhbiV0#=cCb-oi~CJGq*eiGs#{0B3Yl7lXYxxqgsimMSxeKuUDNBbvW4dy#0MnU?Xtm1wxU%(8>Ufce+R{2MwPBady0Szvhzx7BkW>JDOT6jIq)&hj=|fhmG(9VtW!#H7gxf{qRL9EXSaO$RtC~qB#fZSx5ZL#8<{g=y%FG7Gfwf^>)Uy3!WjTJ3tQ4Kd7^*MbHAL?1DeGsZszR`hMlI67581ggb@+9v-LRhW(h@!iz@5XyJ2d54d&G1V$)VGWl~GTmWEmFQ-!%K^q^||6x9!^*NfNOAyEYiC9S-5@*Q+FHP_(V#B{1(y4H-lrADPpIWLys-lP`qIvKCt6D#B&MNWssmFfOvdOCK!}GmAF@YNP<i~|T-(NcRO$Y<}*FS-c!0O4*bhQ~T&XXLqSt$B@{EygFU79qsF3hCjS$qVNwmLclesk13JAE72f1mIVM2itnutirS>hl8TeR#g@?=b4mAU`&$x4CWnFTXY~bq7X`-xb^}C|A(iG969ss3<Q3f$Fb4(w~q2n{g=g%-;bi6oGsxC~=`#p^JfS9~*AR|J|d>iM(Vth1E+23<B`Fpt#lTw{j`_{M*xe&l4_(%4;zb8sIu1pJ{>ZQl2{hUSOa-8>y2e2$3%AfA%|`TrO%|q4h&v!{tjGq>G7}l5vsrjQytif&f#{wV_T43fF9Jk$MdZsxdGKYq1o`4`t?PW{6)HqCUzxsHlbGKJX`Xh|<;b@8fWLk6bclaw1_31e7y8|EeSuNbBN`3iBkrmCN8&T%{gt32)^SQen>2TZl_|o-00mQ7m*^=01=RNN9k3m-~o<s)*{*pesL0BgG|WN<-Z*6<(7o)m9x(H1lp4Wxldz0pVtl<PKcXwh$tOs@Kc{X=Z=WqqZD9&4w!3<@8%N16hP4RBD2_{xU93N^|(Hr0qqyKY4cPQFTWFoL^Jd18^JzCd^C^&yk|Cu?UvdNRdT7lxvi-&EEO3=>@p65jrvDJjTD9R2N22&B!GcO2JbWhW4I1hft;hHLyT+01KAF?Nk#Mw3>Q?)A+j7v559EQK0syI|QK<R3Kg7f7H*mju+9ZC@;4SNmEAj7cQ-qAeCja4Kz=>WJ6jr(Hx9)8}r{`O8;>&%=!&r<f7qh9A9qiV-Wf=esvLKfZ9ciI+;HwgT`rbCVEE5=R_1(8SD@;xO+$D!?>2)Mrsu=mhif9a+j)*UU$H2SXapEtczsIv#f}MD3e?Ac-02rVy|3n|9Ux3Y^9)OYbld@2~Gngb}&jN;jsmZAfduHMaV6Ye`m$7(BT|UcZ<bK&a^6vmCD?bH5zbiHk=;CXV8k3D^qYee*7XI{oqXfsufTk&AAS9f#R-O*NAo<R38K|<zwrXC~&3lXAgk#kxh{Z4<5OxSYHE83>sebIWk2VMssV?yNFAekNaue9SZ$~KIc(V<6bUehz_`l`s*VvWL!?j)PZ%a_dk&aI!hsvS>Q(**M{pvPR~&_1u-#gv`;Iq1~&po{++X(NbtqV0d#UV6VRc+1uwWv{1JJ-1!@Mx*!|*1meYn=Y?ElY_;jO1K;u(9c-p)_eB05kh_Y%Z@~LXBXfRw+5bS$r%z}8M-QR9?i7#PIYJhf@VqZm_ZF!Z_RfUN1mjDkrFzXNUT&sxe)LJTd63!Z+dL6ct1-C*Sk~bH6-*TA(dV3_{ivszdEmya|)p;^s-}Wpj@v|S9IoDqG*tFAdXjDqx=Hqag)+@^#{l39QVTwQS+PY99gPEk3@L-pg?XZ<VH1C`pOQ>>>hHf_MVD1NA+0j`9a1IM*%$Dw6rDCM8iR=C+$6}p;gZYAk45Ejs4an58BR~!6<BRTtO@_!D2Gs~s<ffx82xj3uoVc-;{N-SP$D65z4*?F)drib`#Sa&29#Z@$hvqh>gckHe(ZZPr1gai0tGw;?@E#0Au(X_XAX6ZbnQ&qpepo<{Kt6>y+F7B|KJmeN!wq(BZH>;Lc^e)cusln<b?GfKxTdx6Ft9VWlzfZ<C|i^nV3u?AiZ7YG%RjCBZMOZ3)xT}G&T{aRM`fJf+*%gr?_v7yhU^pPtL#fK?5axxO|1s>cUNI)V@7Ei_dh}g-R4=ZObvtya8F8Yx0e`lIlR%<o9^$UWo<bUr4LLxp)!<#UdHb6Kt&gVv$XX?^Bwf<4sL66EdRAjsjsF1jV^>}B^s+=J6<-Wqa(7kj3DtECye6<2^O3q(&DU=KmQxLmxSE7!gIN4|4nnV5{aWA<1*y4'
    )
_axe_init()
