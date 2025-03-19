#
# spec file for package perl-File-ShareDir-Dist (Version 0.07)
#
# Copyright (c) 125 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%define cpan_name File-ShareDir-Dist
Name:           perl-File-ShareDir-Dist
Version:        0.07
Release:        0%{?autorelease}
License:   Artistic-1.0 or GPL-1.0-or-later
Summary:        Locate per-dist shared files
Url:            https://metacpan.org/release/%{cpan_name}
Source0:         https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/%{cpan_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-macros-suse
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More) >= 0.88
Provides:       perl(File::ShareDir::Dist)
%{?perl_requires}

%description
File::ShareDir::Dist finds share directories for distributions. It is
similar to File::ShareDir with a few differences:

* Only supports distribution directories.

It doesn't support perl modules or perl class directories. I have never
really needed anything other than a per-dist share directory.

* Doesn't compute filenames.

Doesn't compute files in the share directory for you. This is what
File::Spec or Path::Tiny are for.

* Doesn't support old style shares.

For some reason there are two types. I have never seen or needed the older
type.

* Hopefully doesn't find the wrong directory.

It doesn't blindly go finding the first share directory in @INC that
matches the dist name. It actually checks to see that it matches the .pm
file that goes along with it.

That does mean that you need to have a .pm that corresponds to your dist
name. This is not always the case for some older historical distributions,
but it has been the recommended convention for quite some time.

* No non-core dependencies.

File::ShareDir only has Class::Inspector, but since we are only doing
per-dist share directories we don't even need that.

The goal of this project is to have no non-core dependencies for the two
most recent production versions of Perl. As of this writing that means Perl
5.26 and 5.24. In the future, we 'may' add dependencies on modules that are
not part of the Perl core on older Perls.

* Works in your development tree.

Uses the heuristic, for determining if you are in a development tree, and
if so, uses the common convention to find the directory named 'share'. If
you are using a relative path in '@INC', if the directory 'share' is a
sibling of that relative entry in '@INC' and if the last element in that
relative path is 'lib'.

Example, if you have the directory structure:

 lib/Foo/Bar/Baz.pm
 share/data

and you invoke perl with

 % perl -Ilib -MFoo::Bar::Baz -MFile::ShareDir::Dist=dist_share -E 'say dist_share("Foo-Bar-Baz")'

'dist_share' will return the (absolute) path to ./share/data. If you
invoked it with:

 % export PERL5LIB `pwd`/lib
 perl -MFoo::Bar::Baz -MFile::ShareDir::Dist=dist_share -E 'say dist_share("Foo-Bar-Baz")'

it would not. For me this covers most of my needs when developing a Perl
module with a share directory.

prove foils this heuristic by making '@INC' absolute paths. To get around
that you can use App::Prove::Plugin::ShareDirDist.

* Built in override.

The hash '%File::ShareDir::Dist::over' can be used to override what
'dist_share' returns. You can also override behavior on the command line
using a dash followed by a key value pair joined by the equal sign. In
other words:

 % perl -MFile::ShareDir::Dist=-Foo-Bar-Baz=./share -E 'say File::ShareDir::Dist::dist_share("Foo-Bar-Baz")'
 /.../share

If neither of those work then you can set PERL_FILE_SHAREDIR_DIST to a dist
name, directory pair

 % env PERL_FILE_SHAREDIR_DIST=Foo-Bar-Baz=`pwd`/share perl -MFile::ShareDir::Dist -E 'say File::ShareDir::Dist::dist_share("Foo-Bar-Baz")'

For File::ShareDir you have to either mock the 'dist_dir' function or
install File::ShareDir::Override. For testing you can use
Test::File::ShareDir. I have never understood why such a simple concept
needs three modules to do all of this.

%prep
%autosetup  -n %{cpan_name}-%{version} -p1


%build
perl Makefile.PL INSTALLDIRS=vendor
%make_build

%check
make test

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%doc Changes README
%license LICENSE

%changelog
