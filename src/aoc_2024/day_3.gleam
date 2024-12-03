import gleam/bool
import gleam/int
import gleam/list
import gleam/result
import gleam/string

fn r_1(inp: String, acc: Int, enabled: Bool) -> Int {
  case inp {
    "" -> acc
    "don't()" <> rest -> r_1(rest, acc, False)
    "do()" <> rest -> r_1(rest, acc, True)
    "mul(" <> res if enabled -> {
      let next =
        {
          use #(f, _) <- result.try(string.split_once(res, ")"))
          let f = string.split(f, ",")
          use <- bool.guard(list.length(f) != 2, Error(Nil))
          let assert [n1, n2] = f
          use n1 <- result.try(int.parse(n1))
          use n2 <- result.try(int.parse(n2))
          Ok(acc + n1 * n2)
        }
        |> result.unwrap(acc)
      r_1(res, next, enabled)
    }
    _ -> {
      let assert Ok(#(_, r)) = string.pop_grapheme(inp)
      r_1(r, acc, enabled)
    }
  }
}

pub fn pt_1(input: String) {
  r_1(string.replace(input, "do", ""), 0, True)
}

pub fn pt_2(input: String) {
  r_1(input, 0, True)
}
