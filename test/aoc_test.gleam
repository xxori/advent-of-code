import gleeunit
import gleeunit/should

pub fn main() {
  gleeunit.main()
}

pub fn aoc_test() {
  1 + 1 |> should.equal(2)
}
