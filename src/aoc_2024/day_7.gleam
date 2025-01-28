import gleam/int
import gleam/list
import gleam/string

fn is_possible(target: Int, acc: Int, nums: List(Int), concat: Bool) -> Bool {
  case nums {
    [] -> acc == target
    [h, ..t] -> {
      let assert Ok(joined) = int.parse(int.to_string(acc) <> int.to_string(h))
      is_possible(target, acc + h, t, concat)
      || is_possible(target, acc * h, t, concat)
      || { concat && is_possible(target, joined, t, concat) }
    }
  }
}

pub fn parse(input: String) -> List(#(Int, List(Int))) {
  use x <- list.map(string.split(input, "\n"))
  let assert [target, nums] = string.split(x, ":")
  let assert Ok(target) = int.parse(target)
  let nums = nums |> string.split(" ") |> list.filter_map(int.parse)
  #(target, nums)
}

pub fn pt_1(input: List(#(Int, List(Int)))) {
  use acc, x <- list.fold(
    input |> list.filter(fn(x) { is_possible(x.0, 0, x.1, False) }),
    0,
  )
  acc + x.0
}

pub fn pt_2(input: List(#(Int, List(Int)))) {
  use acc, x <- list.fold(
    input |> list.filter(fn(x) { is_possible(x.0, 0, x.1, True) }),
    0,
  )
  acc + x.0
}
