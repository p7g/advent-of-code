import Control.Monad (join)
import Control.Arrow ((***))
import Data.List (dropWhileEnd)

main = do
    input <- lines <$> readFile "input.txt"
    putStrLn . show . uncurry (+) . join (***) abs $ part1 input

data Direction = North | South | East | West

instance Read Direction where
    readsPrec _ (c:cs) = [(dir, cs)]
        where dir = case c of
                      'N' -> North
                      'S' -> South
                      'E' -> East
                      'W' -> West

part1 ls = part2' (0, 0) East instrs
    where instrs = [(c, read cs :: Integer) | c:cs <- ls]

part1' p d instrs =
    case instrs of
      []                -> p
      (('F', n):instrs) -> part2' (move d n p) d instrs
      (('R', n):instrs) -> part2' p (rotateCw n d) instrs
      (('L', n):instrs) -> part2' p d (('R', ccwToCw n):instrs)
      ((d', n):instrs)  -> part2' (move (read [d'] :: Direction) n p) d instrs

    where
        move d n (x, y) = (x + dx d * n, y + dy d * n)

        ccwToCw n = 360 - n

        rotateCw 0 d = d
        rotateCw ndeg d = rotateCw (ndeg - 90) $
            case d of
              North -> East
              East  -> South
              South -> West
              West  -> North

        dx d = case d of
                 East -> 1
                 West -> -1
                 _    -> 0
        dy d = case d of
                 North -> 1
                 South -> -1
                 _    -> 0
