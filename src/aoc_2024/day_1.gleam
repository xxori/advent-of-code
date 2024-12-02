import gleam/dict
import gleam/int
import gleam/list
import gleam/result
import gleam/string

pub fn parse(data: String) -> #(List(Int), List(Int)) {
  data
  |> string.split("\n")
  |> list.map(fn(x) {
    let assert Ok([a, b]) =
      string.split(x, "   ") |> list.map(int.parse) |> result.all
    #(a, b)
  })
  |> list.unzip
}

pub fn pt_1(data: #(List(Int), List(Int))) -> Int {
  let a = list.sort(data.0, int.compare)
  let b = list.sort(data.1, int.compare)
  let pairs = list.zip(a, b)
  use acc, x <- list.fold(pairs, 0)
  acc + int.absolute_value(x.0 - x.1)
}

pub fn pt_2(data: #(List(Int), List(Int))) -> Int {
  let #(first, second) = data
  let freq =
    list.fold(second, dict.new(), fn(acc, x) {
      dict.insert(acc, x, 1 + result.unwrap(dict.get(acc, x), 0))
    })
  use acc, x <- list.fold(first, 0)
  acc + x * result.unwrap(dict.get(freq, x), 0)
}
