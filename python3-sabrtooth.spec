%bcond_without docs

%global srcname sabrtooth
%global _description %{expand:
Imagine having ABRT inside your application and being able to report any runtime
errors on demand. It’s like that, but better.}

Name:      python-%{srcname}
Version:   1.0
Release:   1%{?dist}
Summary:   ABRT: Modular Edition™ for Python
License:   MIT
URL:       https://github.com/abrt/abrt-dev-modules
Source0:   https://github.com/abrt/abrt-dev-modules/archive/%{version}/abrt-dev-modules-%{version}.tar.gz
BuildArch: noarch

%description %{_description}

%package -n python3-%{srcname}

Summary:       %{summary}
BuildRequires: python3-devel

%{?python_enable_dependency_generator}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %{_description}

%package -n python3-%{srcname}-docs

Summary: Documentation for sABRTooth
BuildRequires: %{py3_dist sphinx}
Requires:      python3-%{srcname} = %{version}

%description -n python3-%{srcname}-docs
Documentation for sABRTooth

%prep
%autosetup

%build
%py3_build

%install
%py3_install
%if %{with docs}
%{__python3} -m sphinx %{_smp_mflags} -b devhelp -E docs %{buildroot}%{_datadir}/gtk-doc/html/sABRTooth/
rm -f %{buildroot}%{_datadir}/gtk-doc/html/sABRTooth/.buildinfo
rm -rf %{buildroot}%{_datadir}/gtk-doc/html/sABRTooth/.doctrees/
%endif

%check


%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/sabrtooth/
%{python3_sitelib}/sabrtooth-*.egg-info/

%if %{with docs}
%files -n python3-%{srcname}-docs
%dir %{_datadir}/gtk-doc/html/sABRTooth/
%doc %{_datadir}/gtk-doc/html/sABRTooth/*
%endif

%changelog
