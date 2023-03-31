/**************************************************** scala collection ********************************************************/
// Array
val arr = Array("a", "b", "b", "b", "c", "c")
arr.groupBy(identity).mapValues(_.size).toSeq.sortBy(_._2).reverse.map(_._1).take(3)


// Seq
val seq = Seq(("DEPT1", 1000), ("DEPT1", 500), ("DEPT1", 700), ("DEPT2", 400), ("DEPT2", 200),  ("DEPT3", 500), ("DEPT3", 200))
seq.map(e => (e._1, e._2 + 100))
seq.toMap
seq(2).getClass

val seq2 = ("DEPT0", 400) +: seq :+ ("DEPT4", 300)
val seq3 = seq ++ seq2


// ArrayBuffer
import scala.collection.mutable.ArrayBuffer
val arr = ArrayBuffer(1, 2, 3)
arr += 4


// Set 
import scala.collection.mutable.Set
val set = Set(1, 2, 3, 4)
set -= 4
set --= List(2, 3)

// Map
import scala.collection.mutable.Map
val map = Map("AL" -> "Alabama")
map += ("AR" -> "Arkansas")
map -= "AL"
map.get("AR")    // Option[T]
map.getOrElse("IL", "Not Found")



// function
def topKFrequent(nums: Array[String], k: Int): Array[String] = {
  nums
  .groupBy(identity)
  .mapValues(_.size)
  .toArray
  .sortBy(_._2)
  .reverse
  .map(_._1)
  .take(k)
}
topKFrequent(nums, k)


// recursion and tail recursion
def factorial(n: Int): Int = {
  if (n <= 1) 1
  else n * factorial(n - 1)
}

import scala.annotation.tailrec
def tailRecFactorial(n: Int): BigInt = {
    @tailrec
    def factorialHelper(x: Int, accumulator: BigInt): BigInt = {
      if (x <= 1) accumulator
      else factorialHelper(x - 1, x * accumulator)
    }
    factorialHelper(n, 1)
  }

// level order traversal
object Solution {
  def levelOrder(root: TreeNode): List[List[Int]] = levelOrder(Option(root).toList)

  @scala.annotation.tailrec
  private def levelOrder(nodes: List[TreeNode], traversal: List[List[Int]] = List()): List[List[Int]] = {
    if (nodes.nonEmpty) {
      levelOrder(nodes.flatMap(node => Seq(Option(node.left), Option(node.right)).flatten), traversal :+ nodes.map(_.value))
    } else {
      traversal
    }
  }
}

