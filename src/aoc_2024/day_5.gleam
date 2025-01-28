import aoc_2024/util
import gleam/bool
import gleam/dict.{type Dict}
import gleam/int
import gleam/list
import gleam/option
import gleam/order.{type Order}
import gleam/set.{type Set}
import gleam/string

pub fn parse(input: String) -> #(Dict(Int, Set(Int)), List(List(Int))) {
  let assert [ordering, instructions] = string.split(input, "\n\n")
  let orders = ordering |> string.split("\n") |> list.map(string.split(_, "|"))
  let mapping =
    list.fold(orders, dict.new(), fn(acc, x) {
      let assert [x, y] = list.filter_map(x, int.parse)
      dict.upsert(acc, x, fn(x) { option.unwrap(x, set.new()) |> set.insert(y) })
    })
  let instructions =
    instructions
    |> string.split("\n")
    |> list.map(fn(x) { x |> string.split(",") |> list.filter_map(int.parse) })
  #(mapping, instructions)
}

fn cmp(mapping: Dict(Int, Set(Int)), x: Int, y: Int) -> Order {
  use <- bool.guard(
    dict.get(mapping, x) |> util.is_ok_and(set.contains(_, y)),
    order.Lt,
  )
  use <- bool.guard(
    dict.get(mapping, y) |> util.is_ok_and(set.contains(_, x)),
    order.Gt,
  )
  order.Eq
}

fn work(input: #(Dict(Int, Set(Int)), List(List(Int))), valid: Bool) {
  let #(mapping, instructions) = input
  use acc, x <- list.fold(
    from: 0,
    over: list.filter_map(instructions, fn(x) {
      let sorted = list.sort(x, fn(a, b) { cmp(mapping, a, b) })
      case util.list_eq(x, sorted) == valid {
        True -> Ok(sorted)
        False -> Error(Nil)
      }
    }),
  )
  let assert Ok(mid) = util.get(x, list.length(x) / 2)
  acc + mid
}

pub fn pt_1(input: #(Dict(Int, Set(Int)), List(List(Int)))) {
  work(input, True)
}

pub fn pt_2(input: #(Dict(Int, Set(Int)), List(List(Int)))) {
  work(input, False)
}
