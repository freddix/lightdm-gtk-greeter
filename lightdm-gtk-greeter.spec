Summary:	GTK+ greeter for LightDM
Name:		lightdm-gtk-greeter
Version:	1.6.1
Release:	2
License:	GPL v3
Group:		Themes
Source0:	https://launchpad.net/lightdm-gtk-greeter/1.6/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	a51619d8f85534c22c6d13c8f970fa81
Source1:	background.png
Patch0:		%{name}-config.patch
Patch1:		%{name}-CVE-2014-0979.patch
URL:		https://launchpad.net/lightdm-gtk-greeter
BuildRequires:	gtk+3-devel
BuildRequires:	lightdm-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	gnome-theme-colors-brave
Requires:	gtk+3-theme-greybird
Requires:	lightdm
Provides:	lightdm-greeter
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Reference GTK+ greeter for LightDM.

%prep
%setup -q
%patch0 -p1
%patch1 -p0

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}/lightdm_bg.png

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{lb,mhr,sd,wae}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lightdm/%{name}.conf
%attr(755,root,root) %{_sbindir}/%{name}
%{_datadir}/xgreeters/%{name}.desktop
%{_pixmapsdir}/lightdm_bg.png
#%{_IConsdir}/hicolor/*/places/*.svg

