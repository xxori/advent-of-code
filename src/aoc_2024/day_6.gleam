import aoc_2024/util.{plus}
import gleam/bool
import gleam/io
import gleam/list
import gleam/result
import gleam/set.{type Set}
import gleam/string
import glearray.{type Array}

pub type Cell {
  Obstacle
  Empty
}

pub type Pos =
  #(Int, Int)

fn get_character_pos(grid: List(List(String))) -> Pos {
  use acc, x, r <- list.index_fold(grid, #(-1, -1))
  use <- bool.guard(acc.0 != -1, acc)
  case
    list.index_fold(x, -1, fn(acc2, y, c) {
      use <- bool.guard(acc2 != -1, acc2)
      case y == "^" {
        True -> c
        False -> -1
      }
    })
  {
    -1 -> acc
    c -> #(r, c)
  }
}

pub fn parse(input: String) -> #(Pos, Array(Array(Cell))) {
  let lines = input |> string.split("\n")
  let pos = get_character_pos(lines |> list.map(string.split(_, "")))
  let grid =
    lines
    |> list.map(fn(x) {
      x
      |> string.split("")
      |> list.map(fn(y) {
        case y {
          "#" -> Obstacle
          "." -> Empty
          "^" -> Empty
          _ -> panic as "Unexpected char"
        }
      })
    })
  #(pos, grid |> list.map(glearray.from_list) |> glearray.from_list)
}

fn rot_90(p: Pos) -> Pos {
  case p {
    #(-1, 0) -> #(0, 1)
    #(0, 1) -> #(1, 0)
    #(1, 0) -> #(0, -1)
    #(0, -1) -> #(-1, 0)
    _ -> panic as "Unacceptable direction"
  }
}

fn travel(
  acc: Int,
  visited: Set(Pos),
  grid: Array(Array(Cell)),
  character: Pos,
  direction: Pos,
) -> Int {
  let np = plus(character, direction)
  let seen_np = !set.contains(visited, np) |> bool.to_int
  case
    grid
    |> glearray.get(np.0)
    |> result.then(glearray.get(_, np.1))
  {
    Error(_) -> acc
    Ok(Obstacle) -> travel(acc, visited, grid, character, rot_90(direction))
    Ok(Empty) ->
      travel(acc + seen_np, set.insert(visited, np), grid, np, direction)
  }
}

pub fn pt_1(input: #(Pos, Array(Array(Cell)))) {
  travel(1, set.new() |> set.insert(input.0), input.1, input.0, #(-1, 0))
}

fn does_contain_loops(
  visited: Set(Pos),
  grid: Array(Array(Cell)),
  pos: Pos,
  dir: Pos,
) -> Bool {
  let np = plus(pos, dir)
  case
    grid
    |> glearray.get(np.0)
    |> result.then(glearray.get(_, np.1))
  {
    Error(_) -> False
    Ok(Empty) -> {
      use <- bool.guard(set.contains(visited, np), True)
      does_contain_loops(visited, grid, np, dir)
    }
    Ok(Obstacle) -> {
      does_contain_loops(set.insert(visited, pos), grid, pos, rot_90(dir))
    }
  }
}

fn travel_2(
  acc: Int,
  visited: Set(Pos),
  grid: Array(Array(Cell)),
  pos: Pos,
  dir: Pos,
) -> Int {
  let np = plus(pos, dir)
  case
    grid
    |> glearray.get(np.0)
    |> result.then(glearray.get(_, np.1))
  {
    Error(_) -> acc
    Ok(Obstacle) ->
      travel_2(acc, set.insert(visited, pos), grid, pos, rot_90(dir))
    Ok(Empty) -> {
      let assert Ok(row) = glearray.get(grid, np.0)
      let assert Ok(new_row) = glearray.copy_set(row, np.1, Obstacle)
      let assert Ok(new_grid) = glearray.copy_set(grid, np.0, new_row)
      let obstacle_creates_loop =
        does_contain_loops(visited, new_grid, pos, rot_90(dir)) |> bool.to_int
      case obstacle_creates_loop {
        1 -> io.println("Creates loop at " <> string.inspect(pos))
        _ -> Nil
      }
      travel_2(acc + obstacle_creates_loop, visited, grid, np, dir)
    }
  }
}

pub fn pt_2(input: #(Pos, Array(Array(Cell)))) {
  travel_2(0, set.new(), input.1, input.0, #(-1, 0))
}
