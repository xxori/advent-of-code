import gleam/bool
import gleam/int
import gleam/list
import gleam/result
import gleam/set.{type Set}
import gleam/string
import glearray.{type Array}

pub type Point =
  #(Int, Int)

pub type Grid =
  Array(Array(Int))

pub fn parse(input: String) -> #(Grid, List(Point)) {
  let lines =
    string.split(input, "\n")
    |> list.map(fn(x) { x |> string.split("") |> list.filter_map(int.parse) })
  let starts =
    lines
    |> list.index_fold([], fn(acc, x, r) {
      use acc2, y, c <- list.index_fold(x, acc)
      case y {
        0 -> [#(r, c), ..acc2]
        _ -> acc2
      }
    })
  let grid = lines |> list.map(glearray.from_list) |> glearray.from_list
  #(grid, starts)
}

fn get(grid: Grid, pos: Point) -> Result(Int, Nil) {
  grid
  |> glearray.get(pos.0)
  |> result.then(glearray.get(_, pos.1))
  |> result.replace_error(Nil)
}

fn reachable_nines(grid: Grid, nines: Set(Point), cur: Point) -> Set(Point) {
  let assert Ok(curn) = get(grid, cur)
  // io.println("Visiting " <> string.inspect(cur) <> string.inspect(curn))
  use <- bool.guard(curn == 9, set.insert(nines, cur))
  let rn = glearray.length(grid)
  let assert Ok(cn) = glearray.get(grid, 0) |> result.map(glearray.length)
  [
    #(cur.0, cur.1 + 1),
    #(cur.0, cur.1 - 1),
    #(cur.0 + 1, cur.1),
    #(cur.0 - 1, cur.1),
  ]
  |> list.filter(fn(x) { 0 <= x.0 && x.0 < rn && 0 <= x.1 && x.1 < cn })
  |> list.filter(fn(x) {
    let assert Ok(next) = get(grid, x)
    next == curn + 1
  })
  |> list.fold(nines, fn(acc, x) {
    set.union(acc, reachable_nines(grid, acc, x))
  })
}

pub fn pt_1(input: #(Grid, List(Point))) {
  let #(grid, starts) = input
  use acc, x <- list.fold(starts, 0)
  acc + set.size(reachable_nines(grid, set.new(), x))
}

fn start_rating(grid: Grid, acc: Int, cur: Point) -> Int {
  let assert Ok(curn) = get(grid, cur)
  use <- bool.guard(curn == 9, acc + 1)
  let rn = glearray.length(grid)
  let assert Ok(cn) = glearray.get(grid, 0) |> result.map(glearray.length)
  [
    #(cur.0, cur.1 + 1),
    #(cur.0, cur.1 - 1),
    #(cur.0 + 1, cur.1),
    #(cur.0 - 1, cur.1),
  ]
  |> list.filter(fn(x) { 0 <= x.0 && x.0 < rn && 0 <= x.1 && x.1 < cn })
  |> list.filter(fn(x) {
    let assert Ok(next) = get(grid, x)
    next == curn + 1
  })
  |> list.fold(acc, fn(acc, x) { acc + start_rating(grid, 0, x) })
}

pub fn pt_2(input: #(Grid, List(Point))) {
  let #(grid, starts) = input
  use acc, x <- list.fold(starts, 0)
  acc + start_rating(grid, 0, x)
}
