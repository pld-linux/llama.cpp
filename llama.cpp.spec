# TODO:
# - llguidance support? (-DLLAMA_LLGUIDANCE=ON fetches v1.0.1 from https://github.com/guidance-ai/llguidance, builds with cargo; patch to use system lib?)
# - python tools (using included pyproject.toml)
# - ui (-DLLAMA_BUILD_UI=ON)
Summary:	LLM inference in C/C++
Summary(pl.UTF-8):	Wnioskowanie z użyciem LLM w C/C++
Name:		llama.cpp
Version:	1.0.0
Release:	3
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/ggml-org/llama.cpp/releases
Source0:	https://github.com/ggml-org/llama.cpp/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	688562e96cae0d422272b97afd9ced5f
Patch0:		%{name}-x32.patch
Patch1:		%{name}-32bit.patch
URL:		https://github.com/ggml-org/llama.cpp
BuildRequires:	cmake >= 3.14
BuildRequires:	ggml-devel >= 1.0.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	rpmbuild(macros) >= 1.605
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The main goal of llama.cpp is to enable LLM (and VLM) inference with
minimal setup and state-of-the-art performance on a wide range of
hardware - locally and in the cloud.

%description -l pl.UTF-8
Głównym celem llama.cpp jest, aby umożliwić wnioskowanie z użyciem LLM
(oraz VLM) z minimalną konfiguracją i aktualnie największą wydajnością
na szerokim zakresie sprzętu - lokalnie i w chmurze.

%package libs
Summary:	LLM inference library for C/C++
Summary(pl.UTF-8):	Biblioteka C/C++ do wnioskowania z użyciem LLM
Group:		Libraries

%description libs
LLM inference library for C/C++.

%description libs -l pl.UTF-8
Biblioteka C/C++ do wnioskowania z użyciem LLM.

%package devel
Summary:	Header files for LLaMA libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek LLaMA
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	ggml-devel%{?_isa} >= 1.0.0
Requires:	libstdc++-devel%{?_isa} >= 6:7

%description devel
Header files for LLaMA libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek LLaMA.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%cmake -B build \
	-DLLAMA_TESTS_INSTALL=OFF \
	-DLLAMA_USE_PREBUILT_UI=OFF \
	-DLLAMA_USE_SYSTEM_GGML=ON \

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md SECURITY.md

# app
%attr(755,root,root) %{_bindir}/llama

# examples
%attr(755,root,root) %{_bindir}/llama-batched
# incompatible with GGML_BACKEND_DL, requires GGML_CPU
#%attr(755,root,root) %{_bindir}/llama-convert-llama2c-to-ggml
%attr(755,root,root) %{_bindir}/llama-debug
%attr(755,root,root) %{_bindir}/llama-diffusion-cli
%attr(755,root,root) %{_bindir}/llama-embedding
%attr(755,root,root) %{_bindir}/llama-eval-callback
%attr(755,root,root) %{_bindir}/llama-finetune
%attr(755,root,root) %{_bindir}/llama-gen-docs
%attr(755,root,root) %{_bindir}/llama-gguf
%attr(755,root,root) %{_bindir}/llama-gguf-hash
%attr(755,root,root) %{_bindir}/llama-idle
%attr(755,root,root) %{_bindir}/llama-lookahead
%attr(755,root,root) %{_bindir}/llama-lookup
%attr(755,root,root) %{_bindir}/llama-lookup-create
%attr(755,root,root) %{_bindir}/llama-lookup-merge
%attr(755,root,root) %{_bindir}/llama-lookup-stats
# incompatible with GGML_BACKEND_DL, requires GGML_SYCL
#%attr(755,root,root) %{_bindir}/llama-ls-sycl-device
%attr(755,root,root) %{_bindir}/llama-parallel
%attr(755,root,root) %{_bindir}/llama-passkey
%attr(755,root,root) %{_bindir}/llama-retrieval
%attr(755,root,root) %{_bindir}/llama-simple
%attr(755,root,root) %{_bindir}/llama-simple-chat
%attr(755,root,root) %{_bindir}/llama-speculative
%attr(755,root,root) %{_bindir}/llama-speculative-simple

# pocs, incompatible with GGML_BACKEND_DL, require GGML_CPU
#%attr(755,root,root) %{_bindir}/llama-q8dot
#%attr(755,root,root) %{_bindir}/llama-vdot

# tools
%attr(755,root,root) %{_bindir}/ggml-rpc-server
%attr(755,root,root) %{_bindir}/llama-batched-bench
%attr(755,root,root) %{_bindir}/llama-bench
%attr(755,root,root) %{_bindir}/llama-completion
# incompatible with GGML_BACKEND_DL, require GGML_CPU
#%attr(755,root,root) %{_bindir}/llama-cvector-generator
#%attr(755,root,root) %{_bindir}/llama-export-lora
%attr(755,root,root) %{_bindir}/llama-fit-params
%attr(755,root,root) %{_bindir}/llama-gguf-split
%attr(755,root,root) %{_bindir}/llama-imatrix
%attr(755,root,root) %{_bindir}/llama-mtmd-cli
%attr(755,root,root) %{_bindir}/llama-perplexity
%attr(755,root,root) %{_bindir}/llama-quantize
%attr(755,root,root) %{_bindir}/llama-results
%attr(755,root,root) %{_bindir}/llama-tokenize
%attr(755,root,root) %{_bindir}/llama-tts
%{_libdir}/libllama-batched-bench-impl.so
%{_libdir}/libllama-bench-impl.so
%{_libdir}/libllama-completion-impl.so
%{_libdir}/libllama-fit-params-impl.so
%{_libdir}/libllama-perplexity-impl.so
%{_libdir}/libllama-quantize-impl.so

# tools::server
%attr(755,root,root) %{_bindir}/llama-cli
%attr(755,root,root) %{_bindir}/llama-server
%{_libdir}/libllama-cli-impl.so
%{_libdir}/libllama-server-impl.so

%files libs
%defattr(644,root,root,755)
%{_libdir}/libllama.so.*.*.*
%ghost %{_libdir}/libllama.so.1
%{_libdir}/libllama-common.so.*.*.*
%ghost %{_libdir}/libllama-common.so.1
%{_libdir}/libmtmd.so.*.*.*
%ghost %{_libdir}/libmtmd.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/libllama.so
%{_libdir}/libllama-common.so
%{_libdir}/libmtmd.so
%{_includedir}/llama.h
%{_includedir}/llama-cpp.h
%{_includedir}/mtmd.h
%{_includedir}/mtmd-debug.h
%{_includedir}/mtmd-helper.h
%{_pkgconfigdir}/llama.pc
%{_libdir}/cmake/llama
