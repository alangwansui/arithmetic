#!/usr/bin/py

###_________________________________


I2M = 25.397;      

mode_size=[
[8,    12,    None,  None],
[9,    12,    None,  None],
[9,    16,    None,  None],
[10,   16,    None,  None],
[12,   16,    None,  None],
[12,   18,    None,  None],
[16,   18,    None,  None],
[16,   20,    None,  None],

[12,   20,    None,  None],
[13,   16,    None,  None],
[13.3, 16,    None,  None],
[13.3, 16.3,  None,  None],
[21,   9.6,   None,  None],
[20.5, 9.6,   None,  None],
[18,   9.6,   None,  None],

[13,   12,    None,  None],
[14,   16,    None,  None],
[14,   9.6,   None,  None],
[18.5, 12.2,  None,  None],
[21,   9.6,   None,  None],
];  

margin=[ 
['TOP::MM',  None,],
['BOT::MM',  None,],
['RIG::MM',  None,],
['LEF::MM',  None,],
['SPACE::MM',2 ,],
];

cell=(
 ['UNIT::X:MM', None,],
 ['UNIT::Y:MM', None,],
 ['NUMB::Lay',None],
);

my @title_cn=('ƴ��Inch', 'ƴ��Inch','ƴ����', '������');
my $info;
###__________________________________info genesis

if ( exists_entity('step',"$JOB/pcs") eq 'yes' ) {
	my @prof_limits=prof_limits('pcs','mm');
	($cell[0]->[1],$cell[1]->[1])=( $prof_limits[2] - $prof_limits[0], $prof_limits[3] - $prof_limits[1]);
}elsif ( exists_entity('step',"$JOB/pcb") eq 'yes' ){
	my @prof_limits=prof_limits('pcb','mm');
	($cell[0]->[1],$cell[1]->[1])=( $prof_limits[2] - $prof_limits[0], $prof_limits[3] - $prof_limits[1]);
}else{
	($cell[0]->[1],$cell[1]->[1])=(0,0);
}
$cell[0]->[1]=sprintf('%.2f', $cell[0]->[1] );
$cell[1]->[1]=sprintf('%.2f', $cell[1]->[1] );
$cell[2]->[1]=layer_count($JOB);
if ($cell[2]->[1] >=5) {
		map{ $margin->[$_][1]=18 }(0..3);
}elsif ($cell[2]->[1] >=3){
		map{ $margin->[$_][1]=13 }(0..3);
}else{
		map{ $margin->[$_][1]=8 }(0..3);
};

###___________________________________Tk
my ($col,$row)=(0,0);
my $mw=MainWindow->new;  $mw->geometry("+200+100") ; $mw ->title(encode('utf8',"Better and better"));

foreach  (@{$margin}) {
	$mw->Label(-text=>$_->[0],-relief=>'g',-width=>10)->grid(-column=>$col,-row=>$row++);
	$mw->Entry(-textvariable=>\$_->[1],-relief=>'g',-width=>10)->grid(-column=>$col+1,-row=>$row-1);
}

foreach  (0..$#cell) {
	$mw->Label(-text=>$cell[$_]->[0],-relief=>'g',-width=>10)->grid(-column=>$col+2,-row=>$_);
	$mw->Label(-textvariable=>\$cell[$_]->[1],-relief=>'g',-width=>10)->grid(-column=>$col+3,-row=>$_);
}

foreach my $i (@title_cn) { 
	$mw->Label(-text=>decode('utf8',$i),-width=>10)->grid(-column=>$col++,-row=>$row);
}

foreach  (@$mode_size) {
    $mw->Entry(-textvariable=>\$$_[0],-relief=>'g',-width=>10)->grid(-column=>0,-row=>++$row);
	$mw->Entry(-textvariable=>\$$_[1],-relief=>'g',-width=>10)->grid(-column=>1,-row=>$row);
    $mw->Label(-textvariable=>\$$_[2],-relief=>'g',-width=>10)->grid(-column=>2,-row=>$row);
    $mw->Label(-textvariable=>\$$_[3],-relief=>'g',-width=>10)->grid(-column=>3,-row=>$row);
}
$mw->Label(-textvariable=>\$info,-width=>10,-relief=>'sun',-width=>'42')->grid(-column=>0,-row=>++$row,-columnspan=>5);
$mw->Button(-text=>"Apply",-width=>10,-command=>\&apply)->grid(-column=>0,-row=>++$row);

apply();
MainLoop;

###_______________________________________________________________sub
sub apply {
	if ( $info=check_error() ) {return };
	my ($cell_x,$cell_y,)=($cell[0]->[1],$cell[1]->[1],);
	my ($top,$bot,$rig,$lef,$space)=map{ $margin->[$_][1] }(0..4);
    my $flage=0;
    foreach  (@$mode_size) {
	    my ($px,$py)=( $_->[0], $_->[1] );
	    ($$_[2], $$_[3])=count_pnl($px*I2M,  $py*I2M,  $cell_x, $cell_y, $top, $bot, $rig ,$lef, $space);
		if ( $$_[3] > $flage ){ 
			$flage = $$_[3];
			$info="The max is    ${px}X${py}    $$_[2] pcs    $$_[3] % ";
		};	
	}
}

sub count_pnl {
	my ($px,$py,$cell_x,$cell_y,$top, $bot, $rig ,$lef, $space)=@_;
	my $num_of_not_rotate=count_base($px,$py,$cell_x,$cell_y,$top, $bot, $rig ,$lef, $space);
	my $num_of_yes_rotate=count_base($py,$px,$cell_x,$cell_y,$top, $bot, $rig ,$lef, $space);  ###rotate  px<=>py
	my ($max)=sort{$b<=>$a}($num_of_not_rotate, $num_of_yes_rotate);                           ###save max 
	my $precent=sprintf('%.2f',  ($cell_x*$cell_y*$max)/($px*$py)*100 );                 
	return ( $max,   $precent );
}

sub count_base {
    my ($x,$y,$cell_x,$cell_y,$top, $bot, $rig ,$lef, $space)=@_;
    my ($width,$long)=sort{$a<=>$b}($cell_x,$cell_y);
    my $num_max=0;
    for  (my $i=0;  $i*$long+$lef+$bot+($i-1)*$space <= $x;  $i++) {
	    my $num_r_not=$i * num_of_unitary($y,$width,$space,$top,$bot);  
	    my $res_x;
		($i == 0) ? ($res_x=$x) : ( $res_x=$x-$i*$long-($i-1)*$space );
	    my $num_r_yes= num_of_unitary($res_x,$width,$space,$rig+$space,$lef) * num_of_unitary($y,$long,$space,$top,$bot); 
	    $num_max = ($num_r_yes+$num_r_not) if ($num_r_yes+$num_r_not) > $num_max;  
    }
    return $num_max;
}

sub num_of_unitary {
	my ($long, $cell, $space, $marg_a, $marg_b)=@_;
	my $number=0;
	while (  ($number+1)*$cell + $number*$space + $marg_a + $marg_b <=  $long  ) {
		$number ++;
	}
	return $number;
}

sub check_error {
	foreach  (0..4) {
		if ( $margin->[$_][1] <= 0   or  $margin->[$_][1] =~ m/[^\d\.]/    ) { return "$margin->[$_][0]   Error " }; 
	}
	foreach  (@$mode_size) {
        if (  $$_[0] <= 0  or $$_[0] > 48  or $$_[0]=~m/[^\d\.]/   ) { return "Pnale size Error:: $$_[0] "  };
		if (  $$_[1] <= 0  or $$_[1] > 48  or $$_[1]=~m/[^\d\.]/   ) { return "Pnale size Error:: $$_[1] "  };
	}
}