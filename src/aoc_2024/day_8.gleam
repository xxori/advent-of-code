import aoc_2024/util
import gleam/bool
import gleam/dict
import gleam/list
import gleam/option
import gleam/set.{type Set}
import gleam/string

pub fn parse(input: String) -> #(#(Int, Int), List(List(#(Int, Int)))) {
  let grid = input |> string.split("\n") |> list.map(string.split(_, ""))
  let rn = list.length(grid)
  let cn = list.length(list.first(grid) |> util.unwrap)
  let f =
    list.index_fold(grid, dict.new(), fn(acc, x, r) {
      list.index_fold(x, acc, fn(acc2, y, c) {
        case y {
          "." -> acc2
          _ ->
            dict.upsert(acc2, y, fn(entry) {
              [#(r, c), ..option.unwrap(entry, [])]
            })
        }
      })
    })
  #(#(rn, cn), dict.values(f))
}

pub fn pt_1(input: #(#(Int, Int), List(List(#(Int, Int))))) {
  let #(#(rn, cn), coords) = input
  {
    use acc, nodes <- list.fold(coords, set.new())
    use acc2, n1 <- list.fold(nodes, acc)
    use acc3, n2 <- list.fold(nodes, acc2)
    use <- bool.guard(n1 == n2, acc3)
    let xd = n1.0 - n2.0
    let yd = n1.1 - n2.1
    acc3
    |> set.insert(#(n1.0 + xd, n1.1 + yd))
    |> set.insert(#(n2.0 - xd, n2.1 - yd))
  }
  |> set.filter(fn(n) { 0 <= n.0 && 0 <= n.1 && n.0 < rn && n.1 < cn })
  |> set.size
}

fn loop_2(
  acc: Set(#(Int, Int)),
  cur: #(Int, Int),
  incr: #(Int, Int),
  n: #(Int, Int),
  rn: Int,
  cn: Int,
) -> Set(#(Int, Int)) {
  use <- bool.guard(0 > n.0 || n.0 >= rn || 0 > n.1 || n.1 >= cn, acc)
  let next = #(n.0 + cur.0, n.1 + cur.1)
  let cur = #(cur.0 + incr.0, cur.1 + incr.1)
  loop_2(set.insert(acc, next), cur, incr, next, rn, cn)
}

pub fn pt_2(input: #(#(Int, Int), List(List(#(Int, Int))))) {
  // let antennae =
  //   input.1
  //   |> list.filter(fn(x) { list.length(x) > 1 })
  //   |> list.fold(set.new(), fn(acc, x) { set.union(acc, set.from_list(x)) })
  let #(#(rn, cn), coords) = input
  {
    use acc, nodes <- list.fold(coords, set.new())
    use acc2, n1 <- list.fold(nodes, acc)
    use acc3, n2 <- list.fold(nodes, acc2)
    use <- bool.guard(n1 == n2, acc3)
    let xd = n1.0 - n2.0
    let yd = n1.1 - n2.1
    acc3
    |> loop_2(#(xd, yd), #(xd, yd), n1, rn, cn)
    |> loop_2(#(-xd, -yd), #(-xd, -yd), n2, rn, cn)
  }
  // |> set.union(antennae)
  |> set.size
}
