$fn = 64;
union() {
  translate([0.0, 0.0, -10.0])
  rotate([0.0, 0.0, 0.0])
  scale([1.0, 1.0, 1.0])
  {
    cube([140, 240, 4], center=true);
  }
}

union() {
  translate([-240.0, 0.0, 0.0])
  rotate([0.0, 0.0, 0.0])
  scale([1.0, 1.0, 1.0])
  {
    cube([140, 240, 4], center=true);
  }
}

union() {
  translate([240.0, 0.0, 0.0])
  rotate([0.0, 0.0, 0.0])
  scale([1.0, 1.0, 1.0])
  {
    cube([140, 240, 4], center=true);
  }
}

union() {
  translate([0.0, 0.0, 0.0])
  rotate([0.0, 0.0, 0.0])
  scale([1.0, 1.0, 1.0])
  {
    cube([12, 20, 3], center=true);
    translate([6.0, 0, 5.0]) cube([1, 20, 10.0], center=true);
    translate([-6.0, 0, 5.0]) cube([1, 20, 10.0], center=true);
  }
}

union() {
  translate([0.0, 0.0, 0.0])
  rotate([0.0, 0.0, 0.0])
  scale([1.0, 1.0, 1.0])
  {
    cube([12, 20, 3], center=true);
    translate([6.0, 0, 5.0]) cube([1, 20, 10.0], center=true);
    translate([-6.0, 0, 5.0]) cube([1, 20, 10.0], center=true);
  }
}

union() {
  translate([0.0, 0.0, 0.0])
  rotate([0.0, 0.0, 0.0])
  scale([1.0, 1.0, 1.0])
  {
    cube([12, 20, 3], center=true);
    translate([6.0, 0, 5.0]) cube([1, 20, 10.0], center=true);
    translate([-6.0, 0, 5.0]) cube([1, 20, 10.0], center=true);
  }
}

union() {
  translate([0.0, 0.0, 0.0])
  rotate([0.0, 0.0, 0.0])
  scale([1.0, 1.0, 1.0])
  {
    cube([12, 20, 3], center=true);
    translate([6.0, 0, 5.0]) cube([1, 20, 10.0], center=true);
    translate([-6.0, 0, 5.0]) cube([1, 20, 10.0], center=true);
  }
}

union() {
  translate([0.0, 0.0, 0.0])
  rotate([0.0, 0.0, 0.0])
  scale([1.0, 1.0, 1.0])
  {
    difference() {
      cube([22, 70, 20], center=true);
      translate([0, 0, 2]) cube([18, 66, 20], center=true);
    }
  }
}

union() {
  translate([0.0, 0.0, 0.0])
  rotate([0.0, 0.0, 0.0])
  scale([1.0, 1.0, 1.0])
  {
    difference() {
      cube([22, 70, 20], center=true);
      translate([0, 0, 2]) cube([18, 66, 20], center=true);
    }
  }
}

union() {
  translate([0.0, 0.0, 0.0])
  rotate([0.0, 0.0, 0.0])
  scale([1.0, 1.0, 1.0])
  {
    import("kraft_assembly_1776896366145.stl");
  }
}
