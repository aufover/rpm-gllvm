# https://github.com/SRI-CSL/gllvm/
%global goipath         github.com/SRI-CSL/gllvm
Version:                1.3.0

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
Release:        2%{?dist}
Summary:        Whole Program LLVM: wllvm ported to go
License:        BSD
URL:            %{gourl}
Source0:        %{gosource}

Patch0:         0001-tests-Fix-tests-compatibility-with-gocheck.patch
Patch1:         0001-filetypes.go-Use-absolute-path-to-file.patch

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

# Fix fork bomb in `file`
%patch1 -p1

%build
for cmd in cmd/* ; do
  %gobuild -o %{gobuilddir}/bin/$(basename "$cmd") "%{goipath}/$cmd"
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
* Tue Apr 05 2022 Lukas Zaoral <lzaoral@redhat.com> - 1.3.0-2
- Fix a possible fork bomb during the verification of file package

* Thu Feb 25 2021 Lukas Zaoral <lzaoral@redhat.com> - 1.3.0-1
- New upstream release

* Thu Dec 10 2020 Lukas Zaoral <lzaoral@redhat.com> - 1.2.9-1
- New upstream release

* Thu Oct 29 2020 Lukas Zaoral <lzaoral@redhat.com> - 1.2.8-1
- New upstream release

* Wed Aug 19 2020 Lukas Zaoral <lzaoral@redhat.com> - 1.2.7-1
- First release of gllvm package
