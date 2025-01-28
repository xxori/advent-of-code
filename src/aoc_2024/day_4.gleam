import gleam/bool
import gleam/list
import gleam/result
import gleam/string
import glearray.{type Array}

pub type C {
  X
  M
  A
  S
}

pub type T =
  #(C, #(Int, Int))

const dirs = [
  #(1, 0), #(0, 1), #(1, 1), #(-1, 0), #(0, -1), #(-1, -1), #(1, -1), #(-1, 1),
]

fn try_get(grid, pos: #(Int, Int), f) {
  result.try(
    grid
      |> glearray.get(pos.1)
      |> result.then(glearray.get(_, pos.0))
      |> result.replace_error(0),
    f,
  )
}

fn find_1(grid: Array(Array(T)), tok: T, dir: #(Int, Int)) -> Result(Int, Int) {
  use <- bool.guard(tok.0 == S, Ok(1))
  let to_find = case tok.0 {
    X -> M
    M -> A
    A -> S
    _ -> panic as "unreachable"
  }
  let new_cell = #(tok.1.0 + dir.0, tok.1.1 + dir.1)
  use n <- try_get(grid, new_cell)
  case n.0 == to_find {
    True -> find_1(grid, n, dir)
    False -> Error(0)
  }
}

pub fn parse(input: String) -> Array(Array(T)) {
  input
  |> string.split("\n")
  |> list.index_map(fn(x, i) {
    string.split(x, "")
    |> list.index_map(fn(y, j) {
      let c = case y {
        "X" -> X
        "M" -> M
        "A" -> A
        "S" -> S
        _ -> panic as "Unexpected input"
      }
      #(c, #(j, i))
    })
    |> glearray.from_list
  })
  |> glearray.from_list
}

pub fn pt_1(input: Array(Array(T))) {
  input
  |> glearray.to_list
  |> list.flat_map(glearray.to_list)
  |> list.filter(fn(x) { x.0 == X })
  |> list.fold(0, fn(acc, x) {
    acc
    + list.fold(dirs, 0, fn(acc, y) {
      acc + result.unwrap_both(find_1(input, x, y))
    })
  })
}

fn find_2(grid: Array(Array(T)), loc: #(Int, Int)) -> Result(Int, Int) {
  let #(x, y) = loc
  use ul <- try_get(grid, #(x - 1, y - 1))
  use ur <- try_get(grid, #(x + 1, y - 1))
  use br <- try_get(grid, #(x + 1, y + 1))
  use bl <- try_get(grid, #(x - 1, y + 1))
  let first_mas = { ul.0 == S && br.0 == M } || { ul.0 == M && br.0 == S }
  let second_mas = { ur.0 == S && bl.0 == M } || { ur.0 == M && bl.0 == S }
  case first_mas && second_mas {
    True -> Ok(1)
    False -> Error(0)
  }
}

pub fn pt_2(input: Array(Array(T))) {
  input
  |> glearray.to_list
  |> list.flat_map(glearray.to_list)
  |> list.filter(fn(x) { x.0 == A })
  |> list.fold(0, fn(acc, x) { acc + result.unwrap_both(find_2(input, x.1)) })
}
