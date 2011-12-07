# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section free

Name:           objectweb-asm
Version:        3.1
Release:        7.2%{?dist}
Epoch:          0
Summary:        A code manipulation tool to implement adaptable systems
License:        BSD
URL:            http://asm.objectweb.org/
Group:          Development/Libraries/Java
Source0:        http://download.forge.objectweb.org/asm/asm-3.1.tar.gz
Source1:        http://repo1.maven.org/maven2/asm/asm/3.1/asm-3.1.pom
Source2:        http://repo1.maven.org/maven2/asm/asm-analysis/3.1/asm-analysis-3.1.pom
Source3:        http://repo1.maven.org/maven2/asm/asm-commons/3.1/asm-commons-3.1.pom
Source4:        http://repo1.maven.org/maven2/asm/asm-tree/3.1/asm-tree-3.1.pom
Source5:        http://repo1.maven.org/maven2/asm/asm-util/3.1/asm-util-3.1.pom
Source6:        http://repo1.maven.org/maven2/asm/asm-xml/3.1/asm-xml-3.1.pom
Source7:        http://repo1.maven.org/maven2/asm/asm-all/3.1/asm-all-3.1.pom
Source8:        http://repo1.maven.org/maven2/asm/asm-parent/3.1/asm-parent-3.1.pom
Source9:        asm-MANIFEST.MF
Patch0:         objectweb-asm-no-classpath-in-manifest.patch
# Needed by asm-xml.jar
Requires:       xml-commons-jaxp-1.3-apis
Requires(post): jpackage-utils >= 0:1.7.4
Requires(postun): jpackage-utils >= 0:1.7.4
BuildRequires:  jpackage-utils >= 0:1.7.4
BuildRequires:  java-devel >= 0:1.5.0
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  objectweb-anttask
BuildRequires:  xml-commons-jaxp-1.3-apis
BuildRequires:  zip
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
ASM is a code manipulation tool to implement adaptable systems.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q -n asm-%{version}
%patch0 -p1
perl -pi -e 's/\r$//g' LICENSE.txt README.txt

mkdir META-INF
cp -p %{SOURCE9} META-INF/MANIFEST.MF

%build
export CLASSPATH=
export OPT_JAR_LIST=:
ant -Dobjectweb.ant.tasks.path=$(build-classpath objectweb-anttask) jar jdoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

for jar in output/dist/lib/*.jar; do
install -m 644 ${jar} \
$RPM_BUILD_ROOT%{_javadir}/%{name}/`basename ${jar}`
done

touch META-INF/MANIFEST.MF
zip -u output/dist/lib/all/asm-all-%{version}.jar META-INF/MANIFEST.MF

install -m 644 output/dist/lib/all/asm-all-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/

(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.objectweb-asm-asm.pom
%add_to_maven_depmap org.objectweb.asm asm %{version} JPP/objectweb-asm asm
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-analysis.pom
%add_to_maven_depmap org.objectweb.asm asm-analysis %{version} JPP/objectweb-asm asm-analysis
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-commons.pom
%add_to_maven_depmap org.objectweb.asm asm-commons %{version} JPP/objectweb-asm asm-commons
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-tree.pom
%add_to_maven_depmap org.objectweb.asm asm-tree %{version} JPP/objectweb-asm asm-tree
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-util.pom
%add_to_maven_depmap org.objectweb.asm asm-util %{version} JPP/objectweb-asm asm-util
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-xml.pom
%add_to_maven_depmap org.objectweb.asm asm-xml %{version} JPP/objectweb-asm asm-xml
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-all.pom
%add_to_maven_depmap org.objectweb.asm asm-all %{version} JPP/objectweb-asm asm-all
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-parent.pom
%add_to_maven_depmap org.objectweb.asm asm-parent %{version} JPP/objectweb-asm asm-parent

# javadoc
install -p -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr output/dist/doc/javadoc/user/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt README.txt
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar
%{_datadir}/maven2/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:3.1-7.2
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 23 2008 David Walluck <dwalluck@redhat.com> 0:3.1-5.1
- build for Fedora

* Tue Oct 23 2008 David Walluck <dwalluck@redhat.com> 0:3.1-5
- add OSGi manifest (Alexander Kurtakov)

* Mon Oct 20 2008 David Walluck <dwalluck@redhat.com> 0:3.1-4
- remove Class-Path from MANIFEST.MF
- add unversioned javadoc symlink
- remove javadoc scriptlets
- fix directory ownership
- remove build requirement on dos2unix

* Fri Feb 08 2008 Ralph Apel <r.apel@r-apel.de> - 0:3.1-3jpp
- Add poms and depmap frags with groupId of org.objectweb.asm !
- Add asm-all.jar 
- Add -javadoc Requires post and postun
- Restore Vendor, Distribution

* Thu Nov 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.1-2jpp
- Fix EOL of txt files
- Add dependency on jaxp 

* Thu Nov 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.1-1jpp
- Upgrade to 3.1

* Wed Aug 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.0-1jpp
- Upgrade to 3.0
- Rename to include objectweb- prefix as requested by ObjectWeb

* Thu Jan 05 2006 Fernando Nasser <fnasser@redhat.com> - 0:2.1-2jpp
- First JPP 1.7 build

* Thu Oct 06 2005 Ralph Apel <r.apel at r-apel.de> 0:2.1-1jpp
- Upgrade to 2.1

* Fri Mar 11 2005 Sebastiano Vigna <vigna at acm.org> 0:2.0.RC1-1jpp
- First release of the 2.0 line.
