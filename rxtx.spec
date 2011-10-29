%define version	2.2
%define prerel	pre1
%define upver	%version%{?prerel}
%define rev	20111029
%define mdvrel	1

Name:		rxtx
Version:	%version
Release:	%mkrel %{mdvrel}%{?prerel:.%prerel}%{?rev:.%rev}
Summary:	Serial and parallel I/O libraries supporting Sun's CommAPI
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.rxtx.qbang.org/
#Source0:	http://rxtx.qbang.org/pub/rxtx/%{name}-%{upver}.zip
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  cvs -d:pserver:anonymous@qbang.org:/var/cvs/cvsroot co -r commapi-0-0-1 -D "2011-10-29" -d rxtx-2.2pre1 rxtx-devel
#  tar cjvf rxtx-2.2pre1.tar.bz2 --exclude CVS --exclude .cvsignore rxtx-2.2pre1
Source0:	%{name}-%{upver}.tar.bz2
Patch0:		rxtx-2.2pre1-fc-loadlibrary.patch
Patch1:		rxtx-2.2pre1-mdv-all-ports.patch
Patch2:		rxtx-2.2pre1-mdv-link-math.patch
BuildRequires:	java-devel >= 0:1.6.0

%description
RXTX is a native library providing serial and parallel communication for the
Java Development Toolkit (JDK) moving towards compliance with Sun's CommAPI.

%prep
%setup -q -n %{name}-%{upver}
sed -e 's|@JNIPATH@|%{_jnidir}|' %{PATCH0} | patch -s -b --suffix .p0 -p1
%patch1 -p1
%patch2 -p1
# remove prebuilt binaries
find . -name '*.jar' -delete
find . -name '*.hqx' -delete

%build
%configure2_5x
make
iconv -f ISO_8859-1 -t UTF-8 ChangeLog >ChangeLog.utf-8
mv ChangeLog.utf-8 ChangeLog

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_libdir}
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_jnidir}
make RXTX_PATH=%{buildroot}%{_jnidir} JHOME=%{buildroot}%{_javadir} install
find %{buildroot} -name '*.la' -exec rm {} \;

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README TODO COPYING
%doc RMISecurityManager.html SerialPortInstructions.txt
%{_javadir}/RXTXcomm.jar
%{_jnidir}/*.so
