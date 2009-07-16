%define upstream_version 2.1-7r2
%define major   2.1
%define minor   7
%define libname %mklibname rxtx %{major}
%define develname %mklibname rxtx -d

Name:           rxtx
Version:        2.1.7r2
Release:        %mkrel 1
Summary:        serial and parallel I/O libraries supporting Sun's CommAPI
Group:          System/Libraries
License:        LGPLv2+
URL:            http://www.rxtx.org/
Source0:        http://rxtx.qbang.org/pub/rxtx/%{name}-%{upstream_version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
RXTX is a native library providing serial and parallel communication for the
Java Development Toolkit (JDK) moving towards compliance with Sun's CommAPI.

%package -n %{develname}
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       pkgconfig
Requires:       %{libname} = %{version}-%{release}

%description -n %{develname}
This package contains libraries and header files for
developing applications that use %{name}.

%package -n %{libname}
Summary:        Libraries for %{name}
Group:          System/Libraries

%description -n %{libname}
The libraries for %{name}.

%prep
%setup -q -n %{name}-%{upstream_version}

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_libdir}
install -d -m 755 %{buildroot}%{_datadir}/java
%__make install \
    RXTX_PATH=%{buildroot}%{_libdir} \
    JHOME=%{buildroot}%{_datadir}/java

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README TODO COPYING
%doc RMISecurityManager.html SerialPortInstructions.txt
%{_datadir}/java/RXTXcomm.jar

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*-%{major}-%{minor}.so

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.la
%exclude %{_libdir}/*-%{major}-%{minor}.so

