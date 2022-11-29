%global commit e1ac69b17da0c6d4f5e34e686690ff70c6a43e6f

Name:           gn
Version:        1.0.0
Release:        1
Summary:        Meta-build system that generates build files for Ninja
License:        BSD-3-Clause
URL:            https://gn.googlesource.com/gn
Source0:        %{url}/+archive/gn-%{commit}.tar.gz
Source1:        last_commit_position.h
Patch0:         gn-always-python3.patch

BuildRequires:  python3-devel ninja-build gcc-c++ clang emacs-common help2man

Requires:       vim-filesystem
Requires:       python3
Provides:       vim-gn = %{version}-%{release}
Requires:       emacs-filesystem >= %{_emacs_version}
Provides:       emacs-gn = %{version}-%{release}
Provides:       bundled(icu) = 60

%description
GN is a meta-build system that generates build files for Ninja.


%package doc
Summary:        Documentation for GN
BuildArch:      noarch

%description doc
The gn-doc package contains detailed documentation for GN.


%prep
%autosetup -c -n gn-%{commit} -p1

mkdir -p ./out
cp -vp '%{SOURCE1}' ./out

cp -vp misc/vim/README.md README-vim.md


%build
AR='gcc-ar'; export AR
%set_build_flags
%{__python3} build/gen.py \
    --no-last-commit-position \
    --no-strip \
    --no-static-libstdc++
ninja -C out -v

help2man \
    --name='%{summary}' \
    --version-string="gn $(./out/gn --version)" \
    --no-info \
    ./out/gn |
  tr -d '\302\240' |
  sed -r -e 's/(^[[:alnum:]_]+:)/.TP\n.B \1\n/' \
      -e 's/\[([^]]+)\]/\\fI[\1]\\fR/g' > out/gn.1


%install
install -t '%{buildroot}%{_bindir}' -D -p out/gn

install -d '%{buildroot}%{_datadir}/vim/vimfiles'
cp -vrp misc/vim/* '%{buildroot}%{_datadir}/vim/vimfiles'
find '%{buildroot}%{_datadir}/vim/vimfiles' \
    -type f -name 'README.*' -print -delete
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/vim/vimfiles/gn-format.py

install -t '%{buildroot}%{_emacs_sitestartdir}' -D -p -m 0644 misc/emacs/*.el

install -t '%{buildroot}%{_mandir}/man1' -D -m 0644 -p out/gn.1
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/__pycache__

%check
out/gn_unittests


%files
%license LICENSE
%{_bindir}/gn
%{_mandir}/man1/gn.1*
%{_datadir}/vim/vimfiles/gn-format.py
%{_datadir}/vim/vimfiles/autoload/gn.vim
%{_datadir}/vim/vimfiles/ftdetect/gnfiletype.vim
%{_datadir}/vim/vimfiles/ftplugin/gn.vim
%{_datadir}/vim/vimfiles/syntax/gn.vim
%{_emacs_sitestartdir}/gn-mode.el

%files doc
%license LICENSE src/base/third_party/icu/README.chromium
%doc AUTHORS
%doc OWNERS
%doc README*.md
%doc docs
%doc examples
%doc infra
%doc tools


%changelog
* Tue Nov 29 2022 xuchongyu <xuchongyu@huawei.com> 1.0.0-1
- init
