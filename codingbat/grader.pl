#!/usr/bin/perl
use strict;
use warnings;

use WWW::Mechanize;
use HTTP::Cookies;

sub input {
  print shift.' ';
  system ('stty','-echo') if $_[0] == 1;
  my $response = <STDIN>;
  system ('stty','echo') if $_[0] == 1;
  print "\n" if shift == 1;
  chomp $response;
  return shift if length ($response) == 0;
  return $response;
}

my $db_fn = input ('Database ["students.dat"]:', 0, "students.dat");
my @raw_students = `cat $db_fn`;
$raw_students[$_] = [split (/\W/, $raw_students[$_])] foreach 0..$#raw_students;

my $uname = input ('Username ["utcs303e@yahoo.com"]:', 0, 'utcs303e@yahoo.com');
my $pw = input ('Password:', 1, '');

my $url_root = 'http://www.codingbat.com';
my $url_report = 'http://www.codingbat.com/report';
my $browser = WWW::Mechanize->new ();
$browser->cookie_jar (HTTP::Cookies->new ());
$browser->get ($url_root);
$browser->submit_form (
    with_fields => {
        uname => $uname,
        pw => $pw,
        fromurl => '/'
    }
);
$browser->get ($url_report);
my $raw_user_page = $browser->content();
my @raw_table = $raw_user_page =~ /<tr>.*?'(\/done\?.*?)'.*?<td>(.*?)<\/td>.*?<\/tr>/g;
my %users = (@raw_table);

foreach my $student_ref (@raw_students) {
  my @info = @{$student_ref};
  $info[$_] = lc ($info[$_]) foreach 0..$#info;
  my @possibilites = [];
  my $bestmatch;
  my $bestnum = 0;
  foreach my $key (keys %users) {
    my $tempnum = 0;
    my $templc = lc ($key);
    my $templc_v = lc ($users{$key});
    foreach my $req (@info) {
      $tempnum++ if $templc =~ /\Q$req\E/;
      $tempnum++ if $templc_v =~ /\Q$req\E/;
      $tempnum++ if $req =~ /\Q$templc\E/;
      $tempnum++ if $req =~ /\Q$templc_v\E/;
    }
    ($bestmatch, $bestnum) = ($key, $tempnum) if $tempnum > $bestnum;
  }
  print "$info[0], $info[1]\t".(defined($bestmatch) ? $bestmatch : "---------------------------------------------------")."\n";
}
