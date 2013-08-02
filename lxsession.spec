#
# Conditional build:
%bcond_with		gtk3		# build GTK+3, disables GTK+2
%bcond_without		gtk2	# build with GTK+2

%if %{with gtk3}
%undefine	with_gtk2
%endif

Summary:	Default session manager for LXDE
Name:		lxsession
Version:	0.4.9.2
Release:	3
License:	GPL v2
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
# Source0-md5:	bc3eb71936dbdf813e9ac2f00ab948f0
URL:		http://wiki.lxde.org/en/LXSession
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
%{?with_gtk2:BuildRequires:	gtk+2-devel >= 2:2.12.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel}
BuildRequires:	intltool
BuildRequires:	libgee0.6-devel
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel
BuildRequires:	vala
BuildRequires:	xorg-lib-libX11-devel
Provides:	lxpolkit = 0.1.0-2
Provides:	lxsession-edit = 0.2.0-3
Obsoletes:	lxpolkit
Obsoletes:	lxsession-edit
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LXSession is the default session manager of LXDE.

LXSession automatically starts a set of applications and sets up a
working desktop environment. Moreover, the session manager is able to
remember the applications in use when a user logs out and to restart
them the next time the user logs in.

%prep
%setup -q

%build
%configure \
	%{?with_gtk3:--enable-gtk3}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{frp,ur_PK,tt_RU}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/lxclipboard
%attr(755,root,root) %{_bindir}/lxlock
%attr(755,root,root) %{_bindir}/lxpolkit
%attr(755,root,root) %{_bindir}/lxsession*
%{_datadir}/lxsession
%{_desktopdir}/lxsession*.desktop
%{_mandir}/man1/lxsession*
