%global srcname sabrtooth
%global _description %{expand:
Imagine having ABRT inside your application and being able to report any runtime
errors on demand. It’s like that, but better.}

Name:           python-%{srcname}
Version:        1.0
Release:        1%{?dist}
Summary:        ABRT: Modular Edition™ for Python

License:        MIT
URL:            https://github.com/abrt/abrt-dev-modules
Source0:        https://github.com/abrt/abrt-dev-modules/archive/%{version}/abrt-dev-modules-%{version}.tar.gz

BuildArch:      noarch

%description %{_description}

%package -n python3-%{srcname}

Summary:        %{summary}

BuildRequires:  python3-devel
%{?python_enable_dependency_generator}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %{_description}

%prep
%autosetup

%build
%py3_build

%install
%py3_install

%check


%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/sabrtooth/
%{python3_sitelib}/sabrtooth-*.egg-info/

%changelog
