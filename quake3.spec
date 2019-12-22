Name:           quake3
Version:        1.32
Release:        9%{?dist}
# Required for overriding official package
Epoch:          1
Summary:        Quake III Arena
License:        Proprietary
URL:            http://www.idsoftware.com/
BuildArch:      noarch

Source0:        %{name}.tar.gz
# Quake 3: Retail game data
Source1:        %{name}-pak0.pk3
Source2:        %{name}-docs.tar.gz
# Quake 3 TA: Retail game data
Source3:        %{name}-ta-pak0.pk3
Source4:        %{name}-ta-docs.tar.gz
# Patch files + extras
Source5:        %{name}-%{version}.tar.gz
Source6:        TA_mappak1b.zip
Source7:        TA_mappak2.zip
Source8:        ta_team_titans.zip

NoSource:       1
NoSource:       3

BuildRequires:  desktop-file-utils
BuildRequires:  zip
Requires:       %{name}-engine >= %{version}

%description
Welcome to the Arena, where high-ranking warriors are transformed into
spineless mush. Abandoning every ounce of common sense and any trace of doubt,
you lunge onto a stage of harrowing landscapes and veiled abysses. Your new
environment rejects you with lava pits and atmospheric hazards as legions of
foes surround you, testing the gut reaction that brought you here in the first
place.

Your new mantra: Fight or be finished. 

%package ta
Summary:        Quake III Team Arena
Requires:       %{name}-engine >= %{version}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description ta
Never before have the forces aligned. United by name and by cause, The Fallen,
Pagans, Crusaders, Intruders, and Stroggs must channel their power into an
allied operation where teamwork is the only method of mass destruction. Four
distinct games test each troop's synthesis and strength to exacting degrees.
Cooperation is the only course of action, and war, the only alternative.
Soldiers once alone in their struggle, now face the Arena as one. 

%prep
%setup -q -c -n quake3 -a 2 -a 4 -a 5 -a 6 -a 7 -a 8
mv md3-TA_Titans.pk3 pak98Sounds_Titans.pk3 missionpack/
mv "missionpack/TA Map Pack 1 Readme" missionpack/MapPack1
mv "missionpack/TA Map Pack 2 Readme" missionpack/MapPack2

# Recompress everything in 1 pk3 (saves 100 mb):

#for game in baseq3 missionpack; do
#       cd $game
#       mkdir temp
#       for i in `ls -1 pak*.pk3 | sort`; do unzip -qod temp $i; done
#       rm -fr temp/vm
#       rm -f pak?.pk3
#       cd temp
#       zip -9r ../pak0.pk3 *
#       cd ..
#       rm -fr temp
#       cd ..
#done

%install
cp -fr usr %{buildroot}

# Quake III
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/%{name}/baseq3/pak0.pk3
install -p -m755 baseq3/*pk3 %{buildroot}%{_datadir}/%{name}/baseq3

# Team Arena
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-ta.desktop
mkdir -p %{buildroot}%{_datadir}/%{name}/missionpack
install -p -m 644 %{SOURCE3} %{buildroot}%{_datadir}/%{name}/missionpack/pak0.pk3
install -p -m755 missionpack/*pk3 %{buildroot}%{_datadir}/%{name}/missionpack
install -p -m755 missionpack/*cfg %{buildroot}%{_datadir}/%{name}/missionpack

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc id_patch_pk3s_Q3A_EULA.txt baseq3/Help
%dir %{_datadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}/baseq3
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%files ta
%doc missionpack/Help Titans_Readme.txt
%doc missionpack/MapPack1 missionpack/MapPack2
%{_bindir}/%{name}-ta
%{_datadir}/%{name}/missionpack
%{_datadir}/applications/%{name}-ta.desktop

%changelog
* Sat Jan 23 2016 Simone Caronni <negativo17@gmail.com> - 1:1.32-9
- Remove obsolete tags.

* Sun Aug 05 2012 Simone Caronni <negativo17@gmail.com> - 1:1.32-8
- Avoid useless unpacking in prep section, install unpacked pk3 directly.

* Tue Jul 17 2012 Simone Caronni <negativo17@gmail.com> - 1:1.32-7
- First build.
- Use epoch 1 to avoid official quake3-demo package obsolescency.
