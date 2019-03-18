Summary:	MATE Terminal Emulator
Summary(pl.UTF-8):	Emulator terminala dla środowiska MATE
Name:		mate-terminal
Version:	1.22.0
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.22/%{name}-%{version}.tar.xz
# Source0-md5:	09b01006076bf16f1f4da589b9698375
Patch0:		wordseps.patch
URL:		http://mate-desktop.org/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	bison
BuildRequires:	dconf-devel >= 0.13.4
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.50.0
BuildRequires:	gtk+3-devel >= 3.22.0
BuildRequires:	intltool >= 0.50.1
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	mate-common
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	sed >= 4.0
BuildRequires:	vte-devel >= 0.48
BuildRequires:	xorg-lib-libSM-devel >= 1.0.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	yelp-tools
Requires:	dconf >= 0.13.4
Requires:	glib2 >= 1:2.50.0
Requires:	gtk+3 >= 3.22.0
Requires:	vte >= 0.48
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Terminal Emulator.

%description -l pl.UTF-8
Emulator terminala dla środowiska MATE.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env python,/usr/bin/python,' mate-terminal.wrapper

%build
mate-doc-common --copy
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-compile \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# not using alternatives in pld, drop
# https://github.com/mate-desktop/mate-terminal/issues/9
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mate-terminal.wrapper

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{es_ES,frp,jv,ku_IQ,nqo,pms}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/help/{es_ES,ku_IQ}

desktop-file-install \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/*.desktop

%find_lang %{name} --with-mate

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-terminal
%{_mandir}/man1/mate-terminal.1*
%{_desktopdir}/mate-terminal.desktop
%{_datadir}/metainfo/mate-terminal.appdata.xml
%{_datadir}/glib-2.0/schemas/org.mate.terminal.gschema.xml
%{_datadir}/mate-terminal
