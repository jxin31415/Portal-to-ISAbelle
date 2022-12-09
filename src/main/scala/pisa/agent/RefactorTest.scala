package pisa.agent


import de.unruh.isabelle.control.Isabelle
import de.unruh.isabelle.mlvalue.Implicits._
import de.unruh.isabelle.pure.Implicits._
import de.unruh.isabelle.pure.ToplevelState
import pisa.server.PisaOS

import scala.concurrent._
import scala.concurrent.ExecutionContext
import scala.concurrent.blocking
import scala.concurrent.ExecutionContext.Implicits._
import scala.util.control.Breaks
import java.util.concurrent.CancellationException
import java.io._
import java.util.Base64
import java.nio.charset.StandardCharsets.UTF_8

object RefactorTest {
  val path_to_isa_bin: String = "/home/qj213/Isabelle2021"
  val working_directory: String = "/home/qj213/afp-2021-10-22/thys/FunWithFunctions"
  val path_to_file: String = "/home/qj213/afp-2021-10-22/thys/FunWithFunctions/FunWithFunctions.thy"
  val theorem_string = "qed"

  def main(args: Array[String]): Unit = {
    val pisaos = new PisaOS(
      path_to_isa_bin=path_to_isa_bin,
      path_to_file=path_to_file,
      working_directory=working_directory
    )
    implicit val isabelle: Isabelle = pisaos.isabelle
    implicit val ec: ExecutionContext = pisaos.ec

    pisaos.step_to_transition_text(theorem_string, after = true)

  }
}