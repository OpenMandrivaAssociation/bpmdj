%define name	bpmdj
%define version	2.4
%define release %mkrel 4

Name: 	 	%{name}
Summary: 	Semi-automated DJ utilities
Version: 	%{version}
Release: 	%{release}

Source:		%{name}-%{version}.source.tar.bz2
Patch:		%name-2.4-docfix.diff
Patch1:         %name-2.4-fix-build.patch
URL:		http://bpmdj.sourceforge.net/
License:	GPL
Group:		Sound
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	qt3-devel
BuildRequires:  alsa-lib-devel

%description
BpmDj is a set of programs that can be used to DJ MP3's. The programs has all
kinds of interesting features such as a fully automatic BPM counter (works on
an algorithm invented by me). It can determine the sound color. It has a full
fledged QT (KDE) based interface. It will help you managing a large amount of
songs and above all it is very robust. The program itself requires the
availability of two DSP devices. This can be either by plugging two soundcards
in one machine or using two machines and playing remotely.

%prep
%setup -q
%patch
%patch1 -p1

%build
export PATH=/usr/lib/qt3/bin:$PATH
export QTDIR=%_prefix/lib/qt3
%make CC="gcc $RPM_OPT_FLAGS" CPP="g++ $RPM_OPT_FLAGS" QT_INCLUDE_PATH="-I$QTDIR/include" QT_LIBRARY_PATH="-L$QTDIR/%_lib" QT_LIBS="-lqt-mt"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
rm -fr $RPM_BUILD_ROOT/%_docdir

#menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): command="kbpm-dj" icon="sound_section.png" needs="x11" title="BPMDJ" longtitle="DJ Software" section="Multimedia/Sound" xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=BPMDJ
Comment=DJ Software
Exec=%{_bindir}/kbpm-dj
Icon=%{name}
Terminal=false
Type=Application
Categories=Qt;AudioVideo;Audio;X-MandrivaLinux-Multimedia-Sound;AudioVideo;Mixer;
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
		
%postun
%clean_menus

%files
%defattr(-,root,root)
%doc authors changelog copyright readme ripping todo
%{_bindir}/*
%{_menudir}/%name
%{_datadir}/applications/mandriva-%{name}.desktop

