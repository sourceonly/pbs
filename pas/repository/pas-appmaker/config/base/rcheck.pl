#!/usr/bin/env perl
#
# © Copyright 2007 - 2014 Altair Engineering, Inc. All rights reserved.
#
# This code is provided “as is” without any warranty, express or implied, or 
# indemnification of any kind. All other terms and conditions are as specified 
# in the Altair PBS EULA.

use strict;
use warnings;

use Getopt::Long;
use Pod::Usage;
use IO::File;
use POSIX;

# subroutine for initial configuration of received options, general
# settings and initialization prior to inspection...
sub init {

    # preamble...
    my %rcheck_obj;

    # define rcheck objects / structures. instantiate the Getopt::Long::Parser
    # class, the PBS class and define the 'working' data structure...
    $rcheck_obj{options} = new Getopt::Long::Parser( config => [ 'no_ignore_case', 'bundling' ] );
    $rcheck_obj{toolbox} = new ToolBox;
    $rcheck_obj{working} = {};

    # command line options configuration...
    $rcheck_obj{options}->getoptions(
        'resources|r=s' => \@{ $rcheck_obj{options}->{resources} },
        'unit|u=s'      => \$rcheck_obj{options}->{unit},
        'file|f=s'      => \$rcheck_obj{options}->{file},
        'server|s=s'    => \$rcheck_obj{options}->{server},
        'total|t'       => \$rcheck_obj{options}->{total},
        'help|?|h'      => \&pod2usage,
    );

    # CONFIGURE OPTIONS - this section handles any default / user requested
    # options that will be required for later use with rcheck...
    while ( my ( $option, $value ) = each %{ $rcheck_obj{options} } ) {

        # if the --unit option was passed...
        if ( $option eq 'unit' ) {

            # option handling...
            unless ( ( defined $value ) and ( $value =~ /^[kmgtp]{0,1}b$/i ) ) {
                $rcheck_obj{options}->{unit} = 'kb';
            }
        }

        # if the --file option was passed...
        if ( $option eq 'file' ) {

            # option handling...
            if ( defined $value ) {
                $rcheck_obj{toolbox}->{pbsnodes} = $rcheck_obj{toolbox}->get_pbsnodes(
                    file          => $rcheck_obj{options}->{file},
                    node_list     => 1,
                    resource_list => 1,
                );
            }
        }

        # if the --server option was passed...
        if ( $option eq 'server' ) {

            # option handling...
            if ( defined $value ) {
                $rcheck_obj{toolbox}->{pbsnodes} = $rcheck_obj{toolbox}->get_pbsnodes(
                    server        => $rcheck_obj{options}->{server},
                    node_list     => 1,
                    resource_list => 1,
                );
            }
        }

        # if the --resources option was passed...
        if ( $option eq 'resources' ) {

            # option handling...
            if ( @{$value} ) {
                @{ $rcheck_obj{options}->{resources} }
                    = split( /,/, join ',', @{ $rcheck_obj{options}->{resources} } );
            }
            else {
                $rcheck_obj{options}->{resources} = [ 'mem', 'ncpus' ];
            }
        }
    }

    # assuming the --file nor --server options have not been passed...
    unless ( ( defined $rcheck_obj{options}->{file} )
        or ( defined $rcheck_obj{options}->{server} ) )
    {

        # allow the PBS class to parse the local complex...
        $rcheck_obj{toolbox}->{pbsnodes}
            = $rcheck_obj{toolbox}->get_pbsnodes( node_list => 1, resource_list => 1 );
    }

    # @ARGV, rcheck doesn't include an option for specific hosts / nodes
    # to query since it allows a space separated list of remaining arguments
    # to be intermixed or ( preferably ) at the end of the command string be
    # used as a list of nodes...
    if (@ARGV) {

        # move the options passed to the rcheck options structure...
        @{ $rcheck_obj{options}->{nodes} } = @ARGV;
    }
    else {

        # get a list of complex-wide nodes via PBS...
        $rcheck_obj{options}->{nodes} = \@{ $rcheck_obj{toolbox}->{get_pbsnodes}->{node_list} };
    }

    # if the requester used --file and --server ( multiple input types ) kindly
    # terminate rcheck prior to the inspection process ( could have mixed results )...
    exit(0) if defined $rcheck_obj{options}->{file} and defined $rcheck_obj{options}->{server};

    # ok, now let's inspect the requested information...
    inspect(%rcheck_obj);

}

# subroutine for the inspection and validation of all requested resources
# and nodes received from the command line prior to preparation...
sub inspect {

    # preamble...
    my %rcheck_obj = @_;
    my ( %resources, %nodes );

    # ACTUAL - working arrays of the actual available resources and nodes...
    my @actual_resources = @{ $rcheck_obj{toolbox}->{get_pbsnodes}->{resource_list} };
    my @actual_nodes     = @{ $rcheck_obj{toolbox}->{get_pbsnodes}->{node_list} };

    # REQUESTED - working arrays of the requested resources and nodes...
    my @requested_resources = @{ $rcheck_obj{options}->{resources} };
    my @requested_nodes     = @{ $rcheck_obj{options}->{nodes} };

    # RESOURCES - inspect the actual resources against those requested...
    for my $actual (@actual_resources) {
        for my $requested (@requested_resources) {

            # convert to lowercase ( since PBS is lowercase sensitive )...
            $requested =~ tr/A-Z/a-z/;

            # if we have a match and it doesn't already exist, append to local hash...
            if ( ( $actual eq $requested ) and ( not exists $resources{$actual} ) ) {
                $resources{$actual} = undef;
            }
        }
    }

    # NODES - inspect the actual nodes against those requested...
    for my $actual (@actual_nodes) {
        for my $requested (@requested_nodes) {

            # convert to lowercase ( since PBS is lowercase sensitive )...
            $requested =~ tr/A-Z/a-z/;

            # if we have a match and it doesn't already exist, append to local hash...
            if ( ( $actual eq $requested ) and ( not exists $nodes{$actual} ) ) {
                $nodes{$actual} = undef;
            }
        }
    }

    # copy the inspected resources / nodes to the rcheck options structure...
    @{ $rcheck_obj{options}->{resources} } = sort keys %resources;
    @{ $rcheck_obj{options}->{nodes} }     = sort keys %nodes;

    # if no 'nodes' and / or 'resources' requested exist on the complex, there
    # really is no need to continue... so, if they do exist let's prepare the
    # requested output. otherwise, exit rcheck...
    @{ $rcheck_obj{options}->{resources} }
        and @{ $rcheck_obj{options}->{nodes} } ? prepare(%rcheck_obj) : exit(0);

}

# subroutine for the sorting, filtering and preparation of the data returned
# by PBS in accordance with the default / requested options...
sub prepare {

    # preamble...
    my %rcheck_obj = @_;

    # begin sorting through the returned output of pbsnodes...
    for my $value ( sort( keys( %{ $rcheck_obj{toolbox}->{pbsnodes} } ) ) ) {
        my ( undef, $node, $attribute ) = split( /\:/x, $value );

        # check the list of nodes requested against the current node being parsed.
        # if the node requested matches an available and actual node ( which it
        # obviously should ) append it to the list...
        for my $node_requested ( @{ $rcheck_obj{options}->{nodes} } ) {
            if ( $node eq $node_requested ) {

                # check the list of resources requested against the current attribute...
                for my $resource ( @{ $rcheck_obj{options}->{resources} } ) {
                    if (   ( $attribute eq "resources_available.$resource" )
                        or ( $attribute eq "resources_assigned.$resource" ) )
                    {

                        # NUMERIC - if this is a standard numeric resource...
                        if ( $rcheck_obj{toolbox}->{pbsnodes}->{$value} =~ /^[0-9]+$/x ) {

                            # assign the value to the working data-structure...
                            $rcheck_obj{working}->{nodes}->{$node}->{$attribute}
                                = $rcheck_obj{toolbox}->{pbsnodes}->{$value};

                            # keep track of which resources are NUMERIC for later use...
                            my ( undef, $resource ) = split( /\./x, $attribute );
                            $rcheck_obj{working}->{numeric_resources}->{$resource} = undef;
                        }

                        # SIZED - if this is a sized resource...
                        elsif (
                            $rcheck_obj{toolbox}->{pbsnodes}->{$value} =~ /^[0-9]+([kmgtp]b|b)+$/x )
                        {
                            $rcheck_obj{toolbox}->{pbsnodes}->{$value}
                                = $rcheck_obj{toolbox}->do_convert_unit(
                                input => $rcheck_obj{toolbox}->{pbsnodes}->{$value},
                                unit  => $rcheck_obj{options}->{unit}
                                );

                            # assign the value to the working data-structure...
                            $rcheck_obj{working}->{nodes}->{$node}->{$attribute}
                                = $rcheck_obj{toolbox}->{pbsnodes}->{$value};

                            # keep track of which resources are SIZED for later use...
                            my ( undef, $resource ) = split( /\./x, $attribute );
                            $rcheck_obj{working}->{sized_resources}->{$resource} = undef;
                        }

                        # STRING - if this is a string variable or boolean...
                        elsif ( $rcheck_obj{toolbox}->{pbsnodes}->{$value} =~ /^[0-9a-zA-Z_]+$/x ) {

                            # we will assign an 'undefined' value here since strings
                            # and booleans aren't supported by rcheck...
                            $rcheck_obj{working}->{nodes}->{$node}->{$attribute} = undef;

                            # keep track of which resources are a STRING for later use...
                            my ( undef, $resource ) = split( /\./x, $attribute );
                            $rcheck_obj{working}->{string_resources}->{$resource} = undef;
                        }
                    }
                }
            }
        }
    }

    # for various reasons, the pbsnodes output sometimes won't display any
    # information for a node attribute.  to fight against this, we assign a
    # value of 0 to these empty attributes...
    for my $node ( sort( keys( %{ $rcheck_obj{working}->{nodes} } ) ) ) {
        for my $resource ( @{ $rcheck_obj{options}->{resources} } ) {

            # unless of course this is a string / boolean resource which has
            # no numeric or sized value, so no corrections required...
            unless ( exists $rcheck_obj{working}->{string_resources}->{$resource} ) {

                # for those 'available' resources that had a null value...
                if (not defined $rcheck_obj{working}->{nodes}->{$node}
                    ->{"resources_available.$resource"} )
                {
                    $rcheck_obj{working}->{nodes}->{$node}->{"resources_available.$resource"} = 0;
                }

                # for those 'assigned' resources that had a null value...
                if (not defined $rcheck_obj{working}->{nodes}->{$node}
                    ->{"resources_assigned.$resource"} )
                {
                    $rcheck_obj{working}->{nodes}->{$node}->{"resources_assigned.$resource"} = 0;
                }
            }
        }
    }

    # we won't be needing the PBS class anymore...
    delete $rcheck_obj{toolbox};

    # ok, now let's output the requested information...
    output(%rcheck_obj);

}

# subroutine for displaying the data requested and prepared as either
# a totaled ( all nodes ) or individual ( single node ) summary...
sub output {

    # preamble...
    my %rcheck_obj = @_;
    my ( $available, $assigned, $free, $unit );

    # if the --total option WAS passed...
    if ( defined $rcheck_obj{options}->{total} ) {

        # sort through all of the node information collected, once a resource
        # has been found, automatically increment the data for later output...
        for my $node ( sort( keys( %{ $rcheck_obj{working}->{nodes} } ) ) ) {
            for my $resource ( @{ $rcheck_obj{options}->{resources} } ) {

                # unless of course this is a string / boolean resource which
                # can't be incremented, go ahead and total the resource...
                unless ( exists $rcheck_obj{working}->{string_resources}->{$resource} ) {

                    # increment the value of the given available resource...
                    $rcheck_obj{working}->{total}->{"$resource\_available"}
                        += $rcheck_obj{working}->{nodes}->{$node}
                        ->{"resources_available.$resource"};

                    # increment the value of the given assigned resource...
                    $rcheck_obj{working}->{total}->{"$resource\_assigned"}
                        += $rcheck_obj{working}->{nodes}->{$node}->{"resources_assigned.$resource"};
                }
            }
        }

        # prepare the TOTAL gathered information for display and
        # print to the standard output stream in a rounded list...
        for my $resource ( @{ $rcheck_obj{options}->{resources} } ) {

            # NUMERIC - if the resource being displayed is numeric...
            if ( exists $rcheck_obj{working}->{numeric_resources}->{$resource} ) {

                # working variables...
                $available = ceil $rcheck_obj{working}->{total}->{"$resource\_available"};
                $assigned  = ceil $rcheck_obj{working}->{total}->{"$resource\_assigned"};
                $free      = ceil( $available - $assigned );
                $unit      = '';
            }

            # SIZED - if the resource being displayed is sized...
            elsif ( exists $rcheck_obj{working}->{sized_resources}->{$resource} ) {

                # working variables...
                $available = sprintf '%01.2f',
                    $rcheck_obj{working}->{total}->{"$resource\_available"};

                $assigned = sprintf '%01.2f',
                    $rcheck_obj{working}->{total}->{"$resource\_assigned"};

                $free = sprintf '%01.2f', ( $available - $assigned );
                $unit = $rcheck_obj{options}->{unit};

                # let's do some additional modification to these floating points
                # for more accurate and condensed viewing if required...
                if ( $available =~ /[\.00]+$/x ) {
                    ( $available, undef ) = split( /\./x, $available );
                }
                if ( $assigned =~ /[\.00]+$/x ) {
                    ( $assigned, undef ) = split( /\./x, $assigned );
                }
                if ( $free =~ /[\.00]+$/x ) { ( $free, undef ) = split( /\./x, $free ); }
            }

            # STRING - if the resource being displayed is a string...
            elsif ( exists $rcheck_obj{working}->{string_resources}->{$resource} ) {

                # working variables...
                $available = '<string>';    # pretty much unsupported at this point...
                $assigned  = '<string>';    # pretty much unsupported at this point...
                $free      = '<string>';    # pretty much unsupported at this point...
                $unit      = '';
            }

            # newline...
            print "\n";

            # format the output using PRINTF...
            printf STDOUT '%6.6s nodes, [%-8.8s] F: %-14.14s AV: %-14.14s AS: %-14.14s',
                scalar @{ $rcheck_obj{options}->{nodes} },
                $resource, $free . $unit, $available . $unit, $assigned . $unit;
        }
        print "\n";
    }

    # if the --total option WAS NOT passed...
    if ( not defined $rcheck_obj{options}->{total} ) {

        # prepare the INDIVIDUALY gathered information for display and
        # print to the standard output stream one by one...
        for my $node ( sort( keys( %{ $rcheck_obj{working}->{nodes} } ) ) ) {
            for my $resource ( @{ $rcheck_obj{options}->{resources} } ) {

                # NUMERIC - if the resource being displayed is numeric...
                if ( exists $rcheck_obj{working}->{numeric_resources}->{$resource} ) {

                    # working variables...
                    $available = ceil $rcheck_obj{working}->{nodes}->{$node}
                        ->{"resources_available.$resource"};

                    $assigned = ceil $rcheck_obj{working}->{nodes}->{$node}
                        ->{"resources_assigned.$resource"};

                    $free = ceil( $available - $assigned );
                    $unit = '';
                }

                # SIZED - if the resource being displayed is sized...
                elsif ( exists $rcheck_obj{working}->{sized_resources}->{$resource} ) {

                    # working variables...
                    $available = sprintf '%01.2f',
                        $rcheck_obj{working}->{nodes}->{$node}->{"resources_available.$resource"};

                    $assigned = sprintf '%01.2f',
                        $rcheck_obj{working}->{nodes}->{$node}->{"resources_assigned.$resource"};

                    $free = sprintf '%01.2f', ( $available - $assigned );
                    $unit = $rcheck_obj{options}->{unit};

                    # let's do some additional modification to these floating points
                    # for more accurate and condensed viewing if required...
                    if ( $available =~ /[\.00]+$/x ) {
                        ( $available, undef ) = split( /\./x, $available );
                    }
                    if ( $assigned =~ /[\.00]+$/x ) {
                        ( $assigned, undef ) = split( /\./x, $assigned );
                    }
                    if ( $free =~ /[\.00]+$/x ) { ( $free, undef ) = split( /\./x, $free ); }
                }

                # STRING - if the resource being displayed is a string...
                elsif ( exists $rcheck_obj{working}->{string_resources}->{$resource} ) {

                    # working variables...
                    $available = '<string>';    # pretty much unsupported at this point...
                    $assigned  = '<string>';    # pretty much unsupported at this point...
                    $free      = '<string>';    # pretty much unsupported at this point...
                    $unit      = '';
                }

                # newline...
                print "\n";

                # format the output using PRINTF...
                printf STDOUT '%12.12s, [%-8.8s] F: %-14.14s AV: %-14.14s AS: %-14.14s',
                    $node, $resource, $free . $unit, $available . $unit, $assigned . $unit;
            }
            print "\n";
        }
    }

    # all done... :)
    print "\n";
    exit(1);

}

# program start-point...
init();

package ToolBox;

sub new {

    # preamble...
    my ( $class, %params ) = @_;

    # find the location of the pbs.conf file based on the conf file
    # specified, the environment variable set or the standard /etc/ location...
    if ( defined $ENV{PBS_CONF_FILE} ) {
        $params{conf} = hf_parse_conf( input => $ENV{PBS_CONF_FILE} );
    }
    elsif ( -e '/etc/pbs.conf' ) {
        $params{conf} = hf_parse_conf( input => '/etc/pbs.conf' );
    }
    else {
        die "unable to locate the 'pbs.conf' file: $!\n";
    }

    # bless and return the OO goodness =]
    return bless \%params, $class;

}

# method to extract and parse the data recieved from
# the output of the 'pbsnodes -av' command...
sub get_pbsnodes {

    # preamble...
    my ( $self, %params ) = @_;
    my ( $fh_cmd, %struct, $index, $vhost);

    # if a specific input file was passed...
    if ( defined $params{file} ) {

        # open the input file with the IO::File library...
        $fh_cmd = new IO::File "< $params{file}";
    }

    # or if a specific hostname was passed...
    elsif ( defined $params{server} ) {

        # open for the parsing of STDOUT...
        open $fh_cmd,
            $self->{conf}->{pbs_exec} . "/bin/pbsnodes -av -s $params{server} 2> /dev/null |"
            or die "unable to execute the 'pbsnodes' command: $!\n";
    }

    # otherwise, parse the local complex...
    else {

        # open for the parsing of STDOUT...
        open $fh_cmd, $self->{conf}->{pbs_exec} . '/bin/pbsnodes -av 2> /dev/null |'
            or die "unable to execute the 'pbsnodes' command: $!\n";
    }

    $index = 0;
    
    # line by line, read and parse the output...
    while ( my $line = <$fh_cmd> ) {
        $line = hf_format_string( input => $line );

        # assuming that this line is an actual Vhost identifier
        # and NOT a Vhost attribute...
        unless ( $line =~ /\=/x ) {
            
            # well, not entirely a complete assumption.  i want to at least
            # make sure there are 'letters' and / or numbers on this line...
            if ( $line =~ /^\w.*$/x ) {
                $index++;

                $vhost = $line;

                # if the 'node_list' option was passed...
                if ( exists $params{node_list} == 1 ) {
                    $params{scratch}->{node_list}->{$vhost} = undef;
                }
            }
        }
        else {

            # otherwise, this line is an ACTUAL attribute of a Vhost...
            my ( $attribute, $value ) = split( /\=/x, $line );

            # some additional clean-up for better formatting...
            $attribute = hf_format_string( input => $attribute );
            $value     = hf_format_string( input => $value );

            # if the 'resource_list' option was passed, a hash reference in the
            # classes data-structure will be created for external use...
            if ( ( exists $params{resource_list} == 1 ) and ( $attribute =~ /resources/i ) ) {

                # split the resource from the attribute line and append to
                # the classes public scratch space for later manipulation...
                my ( undef, $resource ) = split( /\./x, $attribute );
                $params{scratch}->{resource_list}->{$resource} = undef;
            }

            # if the 'pcpus_list' option was passed, a hash reference in the
            # classes data-structure will be created for external use...
            if ( ( exists $params{pcpus_list} == 1 ) and ( $attribute =~ /pcpus/i ) ) {

                # split the resource from the attribute line and append to
                # the classes public scratch space for later manipulation...
                my ( undef, $core ) = split( /\=/x, $attribute );
                $params{scratch}->{pcpus_list}->{$core} = undef;
            }

            # assign to local structure...
            $struct{"$index\:$vhost\:$attribute"} = $value;
            
        }
    }

    # if the 'node_list' option was passed, copy the nodes gathered
    # earlier and move them to an array for external use...
    if ( exists $params{node_list} == 1 ) {
        @{ $self->{get_pbsnodes}->{node_list} } = sort keys %{ $params{scratch}->{node_list} };
    }

    # if the 'resource_list' option was passed, copy the resources gathered
    # earlier and move them to an array for external use...
    if ( exists $params{resource_list} == 1 ) {
        @{ $self->{get_pbsnodes}->{resource_list} }
            = sort keys %{ $params{scratch}->{resource_list} };
    }

    # if the 'pcpus_list' option was passed, copy the core's gathered
    # earlier and move them to an array for external use...
    if ( exists $params{pcpus_list} == 1 ) {
        @{ $self->{get_pbsnodes}->{pcpus_list} } = sort keys %{ $params{scratch}->{pcpus_list} };
    }

    # thanks for stopping by! =] ...
    undef $fh_cmd;
    return \%struct;

}

# method that receives a sized integer and converts that integer into
# the type of unit specified by the requestor...
sub do_convert_unit {

    # preamble...
    my ( $self, %params ) = @_;

    # tidy the incoming strings up a bit...
    $params{input} = hf_format_string( input => $params{input} );
    $params{unit}  = hf_format_string( input => $params{unit} );

    # if the input matches one of the unit types supported...
    if ( $params{input} =~ /[kmgtp]b|b+$/x ) {

        # convert the incoming integers unit type to kilobytes...
        my $value = hf_convert_kb( input => $params{input} );

        # if the request is for bytes...
        if ( $params{unit} eq 'b' ) { return ( $value * 1024 ); }

        # if the request is for kilobytes...
        if ( $params{unit} eq 'kb' ) { return ($value); }

        # if the request is for megabytes...
        if ( $params{unit} eq 'mb' ) { return ( $value / 1024 ); }

        # if the request is for gigabytes...
        if ( $params{unit} eq 'gb' ) { return ( $value / 1024 / 1024 ); }

        # if the request is for terabytes...
        if ( $params{unit} eq 'tb' ) { return ( $value / 1024 / 1024 / 1024 ); }

        # if the request is for petabytes...
        if ( $params{unit} eq 'pb' ) { return ( $value / 1024 / 1024 / 1024 / 1024 ); }
    }
    return 0;

}

# internal subroutine used to strip, convert and format strings to a simple
# specification in an effort to standardize various pbs related output...
sub hf_format_string {

    # preamble...
    my %params = @_;

    # convert the incoming strings...
    if ( exists $params{input} ) {

        # convert string to lower-case...
        $params{input} =~ tr/A-Z/a-z/;

        # remove leading whitespace from string...
        $params{input} =~ s/^\s+//x;

        # remove trailing whitespace from string...
        $params{input} =~ s/\s+$//x;
    }

    # return the formatted string...
    return $params{input};

}

# internal subroutine used to parse the information collected from the
# pbs.conf file and apply that information to a data structure...
sub hf_parse_conf {

    # preamble...
    my %params = @_;
    my %struct;

    # open the pbs.conf file, sort through elements within
    # and append to the class' object-structure...
    my $PBS_CONF = new IO::File "< $params{input}";
    while ( my $line = <$PBS_CONF> ) {
        $line = hf_format_string( input => $line );

        # if the line contains a PBS environment variable...
        if ( $line =~ /\=/x ) {
            my ( $variable, $value ) = split( /\=/x, $line );

            # assign to local structure...
            $struct{$variable} = $value;
        }
    }
    undef $PBS_CONF;
    return \%struct;

}

# internal subroutine used to convert all incoming sized
# integers into kilobytes for easier calculations...
sub hf_convert_kb {

    # preamble...
    my %params = @_;

    # this could be done WAY better... :(
    my $integer = $params{input};
    my $unit    = $params{input};
    $integer =~ s/[a-z]+$//x;
    $unit    =~ s/^[0-9]+//x;

    # convert from bytes to kilobytes...
    if ( $unit eq 'b' ) { return $integer / 1024; }

    # convert from kilobytes to kilobytes...
    if ( $unit eq 'kb' ) { return $integer; }

    # convert from megabytes to kilobytes...
    if ( $unit eq 'mb' ) { return $integer * 1024; }

    # convert from gigabytes to kilobytes...
    if ( $unit eq 'gb' ) { return $integer * 1024 * 1024; }

    # convert from terabytes to kilobytes...
    if ( $unit eq 'tb' ) { return $integer * 1024 * 1024 * 1024; }

    # convert from petabytes to kilobytes...
    if ( $unit eq 'pb' ) { return $integer * 1024 * 1024 * 1024 * 1024; }

    return 0;

}

1;

__END__

=head1 SYNOPSIS

[-t] [-u <mb>] [-r <res1>,[res2]...[resX]] [node1] ... [nodeX]

  Options:
  
    -h, -?, --help   A brief help / usage message.   
    -r, --resources  A comma separated list of resources to query.
    -u, --unit       Select the returned unit type for sized resources.
    -f, --file       Parse an existing 'pbsnodes -av' output from a file.
    -s, --server     Parse a 'pbsnodes -av' output from a remote pbs server.
    -t, --total      A total of all resources requested.

  Example:  rcheck -t -r res1,res2 node1 node2 node3

=cut
