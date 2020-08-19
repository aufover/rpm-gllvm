# https://github.com/SRI-CSL/gllvm/
%global goipath         github.com/SRI-CSL/gllvm
Version:                1.2.7

%gometa

%global common_description %{expand:
gllvm provides tools for building whole-program (or whole-library) LLVM bitcode
files from an unmodified C or C++ source package.}

%global golicenses    LICENSE
%global godocs        *.md

%global godevelheader %{expand:
# The devel package will usually benefit from corresponding project binaries.
Requires:  %{name} = %{version}-%{release}
}

Name:           gllvm
Release:        1%{?dist}
Summary:        Whole Program LLVM: wllvm ported to go
License:        BSD
URL:            %{gourl}
Source0:        %{gosource}
Patch0:         0001-tests-Fix-tests-compatibility-with-gocheck.patch

BuildRequires: go-rpm-macros

# Needed fot tests
BuildRequires: clang
BuildRequires: llvm

Requires: clang
Requires: llvm

%description
%{common_description}

%gopkg

%prep
%goprep

# Fix gocheck macro
%patch0 -p1
mv tests/* shared

%build
for cmd in cmd/* ; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%check
%gocheck

%files
%license %{golicenses}
%doc %{godocs}
%{_bindir}/*

%gopkgfiles

%changelog
* Wed Aug 19 2020 Lukas Zaoral <lzaoral@redhat.com> - 1.2.7-1
- First release of gllvm package
