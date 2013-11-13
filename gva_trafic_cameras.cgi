#!/usr/bin/perl --
use strict ;
use warnings ;
use CGI ;
use CGI::Carp qw(fatalsToBrowser);

use LWP ;
use Data::Dumper ;
use JSON ;

$|++;

my $q = new CGI ;
# for help, point your browser to 
# 
my $url = "http://ge.ch/ags1/rest/services/SITG/INFOMOBILITE_DATA/MapServer/3/query?outFields=*&where=1%3D1&f=json&returnGeometry=true" ;
my $filename = 'jsonCached.txt' ; # copy this file in the same directory as this script
print "Content-Type: text/html; charset=ISO-8859-1\n\n";
print "<head>" ;
print "<meta http-equiv=\"refresh\" content=\"60\">\n";
print "<title>Traffic Cameras Geneva</title></head>\n";
print "<body>\n";
&printList ;
print "</body>\n";
exit(0);
###############################################################################
sub printList {	
	my $ua = LWP::UserAgent->new( );
	$ua->timeout( 2 ) ;
	my $res = $ua->get( $url );
	my $content ;
	if ( $res->content =~ /Unauthorized access/ ) {		
		open(FILE, $filename) or die "Can't read file '$filename' [$!]\n";  
		$content = <FILE>; 
		close (FILE); 		
	} else {
		$content = $res->content ;
	}
	my $json = JSON->new->utf8;
	my $perl_scalar = $json->decode( $content );		
	my $camPerLine = 3 ;
	my $camCount = 0 ;
	print qq{<table border='0'>};
	foreach my $location ( @{$perl_scalar->{ features }} ) {
		$camCount++ ;
		$camCount = 1 if ( $camCount > $camPerLine ) ;
		print "<tr>" if ( $camCount == 1 ) ;
		print "<td align='center'><b>" ;
		foreach my $dir ( qw(ALLER RETOUR) ) {
			my $caption = $location->{ attributes }->{ NOM } . " - " . $location->{ attributes }->{ "DIRECTION_$dir" } ;
			print "<a href='" . $location->{ attributes }->{ "IMAGE_$dir" } . "'>" ;
			print "<img src='" . $location->{ attributes }->{ "IMAGE_$dir" }  .  "' alt='$caption'/></a><br>" ;
			print "$caption<br>" ;		
		}
		print "</td>" ;
		print "</tr>\n"  if ( $camCount == $camPerLine ) ;
	}    
	print qq{</table>};
}
###############################################################################

