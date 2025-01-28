import gleam/list

pub fn unwrap(r: Result(a, b)) -> a {
  let assert Ok(suc) = r
  suc
}

pub fn plus(a: #(Int, Int), b: #(Int, Int)) -> #(Int, Int) {
  #(a.0 + b.0, a.1 + b.1)
}

pub fn is_ok_and(r: Result(a, b), f: fn(a) -> Bool) -> Bool {
  case r {
    Ok(x) -> f(x)
    Error(_) -> False
  }
}

pub fn list_eq(a: List(a), b: List(a)) -> Bool {
  list.length(a) == list.length(b)
  && list.zip(a, b) |> list.all(fn(x) { x.0 == x.1 })
}

pub fn get(a: List(a), i: Int) -> Result(a, Nil) {
  let i = case i < 0 {
    False -> i
    True -> list.length(a) + i
  }
  case a {
    [] -> Error(Nil)
    [x, ..] if i == 0 -> Ok(x)
    [_, ..rest] -> get(rest, i - 1)
  }
}
