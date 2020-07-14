import sbtassembly.AssemblyPlugin.autoImport.assemblyJarName

name := "gcpscala"
version := "0.1"
scalaVersion := "2.11.12"

val sparkVersion = "2.4.6"

// Provided means these libs are available in the runtime and must not be packaged
// test means do not add it to final jar when packaging
libraryDependencies ++= Seq(
  "com.typesafe" % "config" % "1.4.0",
  "MrPowers" % "spark-fast-tests" % "0.17.1-s_2.11" % Test,
  "org.scalatest" %% "scalatest" % "3.0.1" % Test,
  "org.apache.spark" %% "spark-core" % sparkVersion  % Provided,
  "org.apache.spark" %% "spark-sql"  % sparkVersion  % Provided
)

//TODO -- I cant get the BIG QUERY JAR this to be part of the FAT JAR so i'm having to pass the Jar Manually in my gcloud command
//https://cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example

resolvers ++= Seq(
  "bintray-spark-packages" at "https://dl.bintray.com/spark-packages/maven",
  "Typesafe Simple Repository" at "https://repo1.maven.org/maven2/com/typesafe/config/",
  "MavenRepository" at "https://mvnrepository.com",
  "MavenCentral" at "https://mvnrepository.com/artifact/org.apache.spark/spark-core"
)

// Do not to Include the Scala Binary in the Jar
//assemblyOption in assembly := (assemblyOption in assembly).value.copy(includeScala = false)

// Jar Naming Convention
assemblyJarName in assembly := s"${name.value}-${version.value}.jar"

assemblyMergeStrategy in assembly := {
  case x if x.endsWith("io.netty.versions.properties") => MergeStrategy.first
  case PathList("com",   "google", _*) => MergeStrategy.last
  case PathList("com",   "esotericsoftware", _*) => MergeStrategy.last
  case PathList("io",    "netty", _*) => MergeStrategy.last
  case PathList("org",   "slf4j", _*) => MergeStrategy.last
  case PathList("org",   "apache", _*) => MergeStrategy.last
  case "META-INF/maven/com.google.api.grpc/" => MergeStrategy.last
  case x =>
    val oldStrategy = (assemblyMergeStrategy in assembly).value
    oldStrategy(x)
}