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

my $LANGUAGE = 'python';

my $db_fn = input ('Database ["students.dat"]:', 0, "students.dat");
my @raw_students = `cat $db_fn`;
chomp foreach @raw_students;
$raw_students[$_] = [split (/\W/, $raw_students[$_])] foreach 0..$#raw_students;

my $problems = input ('Problems ["problems.dat"]:', 0, "problems.dat");
my @problems = `cat $problems`;
chomp foreach @problems;

my $out_fn = input ('Output File ["output.dat"]:', 0, "output.dat");
open (my $out_fh, '>', $out_fn);

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
my $raw_user_page = $browser->content ();
my @raw_table = $raw_user_page =~ /<tr>.*?'(\/done\?.*?)'.*?<td>(.*?)<\/td>.*?<\/tr>/g;
my %users = (@raw_table);

my $first_time = 1;

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
  my $grade = 0;
  if ($info[0] ne "false" and defined ($bestmatch)) {
    $browser->get ($url_root.$bestmatch);
    if ($first_time) {
      $browser->submit_form (
          with_fields => {
              showstart => 'off'
          }
      );
      $first_time = 0;
    }
    my $progress_page = $browser->content ();
    foreach my $problem (@problems) {
      $grade += 10 if $progress_page =~ /\Q$problem\E.{0,7}$LANGUAGE/;
    }
  }
  print $out_fh "$info[0]\t$grade\n";
  print "$info[0]: $grade\n" if $info[0] ne "false";
}

close $out_fh;
