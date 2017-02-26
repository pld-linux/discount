Summary:	A command-line utility for converting Markdown files into HTML
Summary(pl.UTF-8):	Działające z linii poleceń narzędzie do konwersji plików Markdown do HTML-a
Name:		discount
Version:	2.2.2
Release:	1
License:	BSD
Group:		Applications/Text
Source0:	http://www.pell.portland.or.us/~orc/Code/discount/%{name}-%{version}.tar.bz2
# Source0-md5:	0531fc428f023942b364c781a948df08
Patch0:		%{name}-ldconfig.patch
URL:		http://www.pell.portland.or.us/~orc/Code/discount
Requires:	libmarkdown = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DISCOUNT is an implementation of John Gruber's Markdown language in C.
It includes all of the original Markdown features, along with a few
extensions, and passes the Markdown test suite.

%description -l pl.UTF-8
DISCOUNT to implementacja języka Markdown Johna Grubera w C. Obejmuje
wszystkie oryginalne cechy języka Markdown wraz z kilkoma
rozszerzeniami, przechodzi zestaw testów Markdown.

%package -n libmarkdown
Summary:	A fast implementation of the Markdown language in C
Summary(pl.UTF-8):	Szybka implementacja języka Markdown w C
Group:		Libraries

%description -n libmarkdown
libmarkdown is the library portion of discount, a fast Markdown
language implementation, written in C.

%description -n libmarkdown -l pl.UTF-8
libmarkdown to biblioteka z projektu discount, będąca szybką
implementacją języka Markdown, napisaną w C.

%package -n libmarkdown-devel
Summary:	Development headers for the libmarkdown library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmarkdown
Group:		Development/Libraries
Requires:	libmarkdown = %{version}-%{release}

%description -n libmarkdown-devel
This package contains development headers and developer-oriented man
pages for libmarkdown.

%description -n libmarkdown-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe oraz dokumentację programisty do
biblioteki libmarkdown.

%prep
%setup -q
%patch0 -p1

%build
# NOTE: not autoconf based configure
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
./configure.sh \
	--shared \
	--prefix=%{_prefix} \
	--execdir=%{_bindir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--enable-all-features \
	--with-fenced-code

%{__make}

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install.everything \
	DESTDIR=$RPM_BUILD_ROOT

# Rename sample programs (names are too generic) and matching man1 pages
%{__mv} $RPM_BUILD_ROOT%{_bindir}/makepage $RPM_BUILD_ROOT%{_bindir}/discount-makepage
%{__mv} $RPM_BUILD_ROOT%{_bindir}/mkd2html $RPM_BUILD_ROOT%{_bindir}/discount-mkd2html
%{__mv} $RPM_BUILD_ROOT%{_bindir}/theme $RPM_BUILD_ROOT%{_bindir}/discount-theme
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/makepage.1 \
	$RPM_BUILD_ROOT%{_mandir}/man1/discount-makepage.1
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/mkd2html.1 \
	$RPM_BUILD_ROOT%{_mandir}/man1/discount-mkd2html.1
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/theme.1 \
	$RPM_BUILD_ROOT%{_mandir}/man1/discount-theme.1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libmarkdown -p /sbin/ldconfig
%postun	-n libmarkdown -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/markdown
%attr(755,root,root) %{_bindir}/discount-makepage
%attr(755,root,root) %{_bindir}/discount-mkd2html
%attr(755,root,root) %{_bindir}/discount-theme
%{_mandir}/man1/markdown.1*
%{_mandir}/man7/markdown.7*
%{_mandir}/man1/discount-*.1*
%{_mandir}/man7/mkd-*.7*

%files -n libmarkdown
%defattr(644,root,root,755)
%doc README COPYRIGHT CREDITS
%attr(755,root,root) %{_libdir}/libmarkdown.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmarkdown.so.2

%files -n libmarkdown-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmarkdown.so
%{_includedir}/mkdio.h
%{_mandir}/man3/markdown.3*
%{_mandir}/man3/mkd_*.3*
%{_mandir}/man3/mkd-*.3*
