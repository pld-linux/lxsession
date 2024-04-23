#
# Conditional build:
%bcond_without	gtk3	# use GTK+3 instead of GTK+2
%bcond_without	notify	# libnotify/indicators based notification

Summary:	Default session manager for LXDE
Summary(pl.UTF-8):	Domyślny zarząda sesji dla LXDE
Name:		lxsession
Version:	0.5.5
Release:	3
License:	GPL v2+
Group:		X11/Applications
Source0:	https://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.xz
# Source0-md5:	e8380acef215ee7c99c067a2241c2c7b
Patch0:		libayatana.patch
Patch1:		no-keyring.patch
URL:		http://www.lxde.org/
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl-nons >= 1.70.1
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.28.0
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.12.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	intltool >= 0.40.0
%if %{with notify}
%{!?with_gtk3:BuildRequires:	libayatana-appindicator-gtk2-devel}
%{?with_gtk3:BuildRequires:	libayatana-appindicator-gtk3-devel}
BuildRequires:	libayatana-indicator-devel
BuildRequires:	libnotify-devel
%endif
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.16.0
%if %{with notify}
%{!?with_gtk3:BuildRequires:	vala-libayatana-appindicator-gtk2}
%{?with_gtk3:BuildRequires:	vala-libayatana-appindicator-gtk3}
%endif
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.12.0}
%{?with_notify:Requires:	libayatana-indicator}
Provides:	lxpolkit = 0.1.0-2
Provides:	lxsession-edit = 0.2.0-3
Obsoletes:	lxpolkit < 0.1.0-2
Obsoletes:	lxsession-edit < 0.2.0-3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LXSession is the default session manager of LXDE.

LXSession automatically starts a set of applications and sets up a
working desktop environment. Moreover, the session manager is able to
remember the applications in use when a user logs out and to restart
them the next time the user logs in.

%description -l pl.UTF-8
LXSession to domyślny zarządca sesji środowiska LXDE.

LXSession automatycznie uruchamia zestaw aplikacji i ustawia
działające środowisko graficzne. Co więcej, zarządca sesji może
pamiętać aplikacje używane w chwili wylogowania użytkownika i
uruchomić je ponownie przy kolejnym zalogowaniu tego użytkownika.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	%{?with_notify:--enable-advanced-notifications} \
	%{?with_gtk3:--enable-gtk3} \
	--disable-silent-rules
# Delete bundled .c files to force regeneration using valac
%{__make} clean-generic
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# unify name
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{tt_RU,tt}
# not supported by glibc
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/frp
# just a copy of ur
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ur_PK

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_bindir}/lxclipboard
%attr(755,root,root) %{_bindir}/lxlock
%attr(755,root,root) %{_bindir}/lxpolkit
%attr(755,root,root) %{_bindir}/lxsession
%attr(755,root,root) %{_bindir}/lxsession-db
%attr(755,root,root) %{_bindir}/lxsession-default
%attr(755,root,root) %{_bindir}/lxsession-default-apps
%attr(755,root,root) %{_bindir}/lxsession-default-terminal
%attr(755,root,root) %{_bindir}/lxsession-edit
%attr(755,root,root) %{_bindir}/lxsession-logout
%attr(755,root,root) %{_bindir}/lxsession-xdg-autostart
%attr(755,root,root) %{_bindir}/lxsettings-daemon
%dir %{_libexecdir}/lxsession
%attr(755,root,root) %{_libexecdir}/lxsession/lxsession-xsettings
/etc/xdg/autostart/lxpolkit.desktop
%{_datadir}/lxsession
%{_desktopdir}/lxsession-default-apps.desktop
%{_desktopdir}/lxsession-edit.desktop
%{_mandir}/man1/lxclipboard.1*
%{_mandir}/man1/lxlock.1*
%{_mandir}/man1/lxpolkit.1*
%{_mandir}/man1/lxsession.1*
%{_mandir}/man1/lxsession-db.1*
%{_mandir}/man1/lxsession-default.1*
%{_mandir}/man1/lxsession-default-apps.1*
%{_mandir}/man1/lxsession-default-terminal.1*
%{_mandir}/man1/lxsession-edit.1*
%{_mandir}/man1/lxsession-logout.1*
%{_mandir}/man1/lxsession-xdg-autostart.1*
%{_mandir}/man1/lxsettings-daemon.1*
