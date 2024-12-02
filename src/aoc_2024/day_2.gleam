import gleam/function
import gleam/int
import gleam/list
import gleam/string

pub fn parse(input: String) -> List(List(Int)) {
  let lines =
    input
    |> string.split("\n")
  use x <- list.map(lines)
  x |> string.split(" ") |> list.filter_map(int.parse)
}

fn is_valid_1(report: List(Int)) -> Bool {
  let diffs = list.window_by_2(report) |> list.map(fn(x) { x.0 - x.1 })
  list.all(diffs, fn(x) { 1 <= x && x <= 3 })
  || list.all(diffs, fn(x) { -3 <= x && x <= -1 })
}

pub fn pt_1(input: List(List(Int))) {
  list.count(input, is_valid_1)
}

fn is_valid_2(report: List(Int)) -> Bool {
  list.range(0, list.length(report) - 1)
  |> list.map(fn(i) {
    let assert Ok(#(_, r)) =
      report
      |> list.index_map(fn(x, i) { #(x, i) })
      |> list.pop(fn(x) { x.1 == i })
    r |> list.map(fn(x) { x.0 }) |> is_valid_1
  })
  |> list.any(function.identity)
}

pub fn pt_2(input: List(List(Int))) {
  list.count(input, is_valid_2)
}
