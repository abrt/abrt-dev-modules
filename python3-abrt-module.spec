Name:           python3-abrt-module
Version:        1.0
Release:        1%{?dist}
Summary:        ABRT: Modular Edition™ for Python

License:        MIT
URL:            https://github.com/abrt/abrt-dev-modules
Source0:        https://github.com/abrt/abrt-dev-modules/archive/%{version}/abrt-dev-modules-%{version}.tar.gz

%{?python_enable_dependency_generator}

%description
Imagine having ABRT inside your application and being able to report any runtime
errors on demand. It’s like that, but better.

%prep
%autosetup

%build
%py3_build

%install
%py3_install

%check


%files
%license LICENSE
%doc README.md
%{python3_sitelib}/abrt-module/
%{python3_sitelib}/abrt-module-*.egg-info/

%changelog
