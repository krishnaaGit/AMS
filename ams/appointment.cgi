#!"C:\Strawberry\perl\bin\perl.exe"

use warnings; 
use strict;
use CGI qw(:standard);
use DBI;
use HTML::Parser;
use JSON;
binmode STDOUT, ":utf8";
use utf8;
 
#connect to the DB
my $driver = "SQLite";
my $database = "appointment.db";
my $dsn = "DBI:$driver:dbname=$database";
my $userid = "";
my $password = "";
my $dbh = DBI->connect($dsn, $userid, $password, {RaiseError=> 1}) or die $DBI::errstr;

my $cgi = new CGI;

print $cgi->header('text/html');


my $dateset = param('app_date') if (param('app_date'));
my $descset = param('description') if (param('description'));
my $searchset ='';
	$searchset = url_param('search') if (url_param('search'));
	
my $stmt = q/create table if not exists appointment (app_date datetime, description varchar(100))/;
my $sth = $dbh->prepare($stmt);
$sth->execute();

# if there is params it's a POST, create new record
if ($dateset && $descset) {
	print $cgi->start_html(-title=>'Appointment Output');
	print "Date: $dateset | Description: $descset will be added to the database";
my $stmt = q/INSERT INTO appointment (app_date, description) VALUES (?,?)/;
	my $sth = $dbh->prepare($stmt);
	$sth->execute($dateset, $descset);
	print "Done!";
	#Reroute to the same page
	print '<meta http-equiv="refresh" content="1;url=http://localhost/ams/">';
	
} else # else it's a get request, list the data
{

	my @output;
	my $stmt = q/select strftime("%m",app_date) month,strftime("%d",app_date) day,strftime("%H",app_date) hour,strftime("%M",app_date) minute, description from appointment where description like ?/;
	my $sth = $dbh->prepare($stmt);
	$sth->bind_param( 1,   "%" .$searchset."%"   );
	$sth->execute;

	while(my $row = $sth->fetchrow_hashref) {
		push @output, $row;
	}
	print to_json({data=> \@output});
}
$dbh->disconnect();
