Summary:	MATE Terminal Emulator
Name:		mate-terminal
Version:	1.6.1
Release:	3
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	c9e1c80d9184aca710e92bd944f2bb7c
Patch0:		wordseps.patch
URL:		http://mate-desktop.org/
BuildRequires:	bison
BuildRequires:	dconf-devel
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	glib2-devel >= 1:2.30
BuildRequires:	gtk+2-devel
BuildRequires:	libxml2-devel
BuildRequires:	mate-common
BuildRequires:	mate-doc-utils
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	vte0-devel
BuildRequires:	xorg-lib-libSM-devel
Requires:	glib2 >= 1:2.26.0
Requires:	mate-desktop
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Terminal Emulator.

%prep
%setup -q
%patch0 -p1

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--disable-silent-rules \
	--disable-schemas-compile

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/*.desktop

%find_lang %{name} --with-mate --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_bindir}/mate-terminal
%{_mandir}/man1/mate-terminal.1*
%{_desktopdir}/mate-terminal.desktop
%{_datadir}/glib-2.0/schemas/org.mate.terminal.gschema.xml
%{_datadir}/mate-terminal
