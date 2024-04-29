#!/bin/sh
#
# Copyright (c) 2012 - 2024 YCSB contributors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License. You
# may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License. See accompanying
# LICENSE file.
#
# -----------------------------------------------------------------------------
# Control Script for YCSB
#
# Environment Variable Prerequisites
#
#   Do not set the variables in this script. Instead put them into a script
#   setenv.sh in YCSB_HOME/bin to keep your customizations separate.
#
#   YCSB_HOME       (Optional) YCSB installation directory. If not set
#                   this script will use the parent directory of where this
#                   script is run from.
#
#   JAVA_HOME       (Optional) Must point at your Java Development Kit
#                   installation. If empty, this script tries use the
#                   available java executable.
#
#   JAVA_OPTS       (Optional) Java runtime options used when any command
#                   is executed.
#
#   WARNING!!! YCSB home must be located in a directory path that doesn't
#   contain spaces.
#
#        www.shellcheck.net was used to validate this script

# Cygwin support
CYGWIN=false
case "$(uname)" in
CYGWIN*) CYGWIN=true;;
esac

# Get script path
SCRIPT_DIR=$(dirname "$0" 2>/dev/null)

# Only set YCSB_HOME if not already set
: "${YCSB_HOME:=$(cd "$SCRIPT_DIR/.." && pwd)}"

# Ensure that any extra CLASSPATH variables are set via setenv.sh
CLASSPATH=

# Pull in customization options
if [ -r "$YCSB_HOME/bin/setenv.sh" ]; then
  # shellcheck source=/dev/null
  . "$YCSB_HOME/bin/setenv.sh"
fi

# Attempt to find the available JAVA, if JAVA_HOME not set
if [ -z "$JAVA_HOME" ]; then
  JAVA_PATH=$(command -v java 2>/dev/null)
  if [ -n "$JAVA_PATH" ]; then
    JAVA_HOME=$(dirname "$(dirname "$JAVA_PATH")")
  fi
fi

# If JAVA_HOME still not set, error
if [ -z "$JAVA_HOME" ]; then
  echo "[ERROR] Java executable not found. Exiting." >&2
  exit 1
fi

# Determine YCSB command argument
case "$1" in
  load)
    YCSB_COMMAND=-load
    YCSB_CLASS=site.ycsb.Client
    ;;
  run)
    YCSB_COMMAND=-t
    YCSB_CLASS=site.ycsb.Client
    ;;
  shell)
    YCSB_COMMAND=
    YCSB_CLASS=site.ycsb.CommandLine
    ;;
  *)
    echo "[ERROR] Found unknown command '$1'" >&2
    echo "[ERROR] Expected one of 'load', 'run', or 'shell'. Exiting." >&2
    exit 1
    ;;
esac

# Find binding information
BINDING_LINE=$(grep "^$2:" "$YCSB_HOME/bin/bindings.properties" -m 1)

if [ -z "$BINDING_LINE" ]; then
  echo "[ERROR] The specified binding '$2' was not found. Exiting." >&2
  exit 1
fi

# Get binding name and class
BINDING_NAME=$(echo "$BINDING_LINE" | cut -d':' -f1)
BINDING_CLASS=$(echo "$BINDING_LINE" | cut -d':' -f2)

# Some bindings have multiple versions that are managed in the same directory.
# They are noted with a '-' after the binding name.
# (e.g. cassandra-7 & cassandra-8)
BINDING_DIR=$(echo "$BINDING_NAME" | cut -d'-' -f1)

# The 'basic' binding is core functionality
if [ "$BINDING_NAME" = "basic" ]; then
  BINDING_DIR=core
fi

# For Cygwin, ensure paths are in UNIX format before anything is touched
if "$CYGWIN"; then
  JAVA_HOME=$(cygpath --unix "$JAVA_HOME")
  CLASSPATH=$(cygpath --path --unix "$CLASSPATH")
fi

# Check if source checkout, or release distribution
DISTRIBUTION=true
if [ -r "$YCSB_HOME/pom.xml" ]; then
  DISTRIBUTION=false
fi

# Add Top level conf to classpath
CLASSPATH="$CLASSPATH:$YCSB_HOME/conf"

# Deprecation messages
case "$BINDING_DIR" in
  cassandra2)
    echo "[WARN] The 'cassandra2-cql' client has been deprecated. It has been renamed to simply 'cassandra-cql'. This alias will be removed in the next YCSB release." >&2
    BINDING_DIR="cassandra"
    ;;
  hbase14)
    echo "[WARN] The 'hbase14' client has been deprecated. HBase 1.y users should rely on the 'hbase1' client instead." >&2
    BINDING_DIR="hbase1"
    ;;
  arangodb3)
    echo "[WARN] The 'arangodb3' client has been deprecated. The binding 'arangodb' now covers every ArangoDB version. This alias will be removed in the next YCSB release." >&2
    BINDING_DIR="arangodb"
    ;;
  couchbase)
    echo "[WARN] The 'couchbase' client is deprecated. If you are using Couchbase 4.0+ try using the 'couchbase2' client instead." >&2
    ;;
esac

# Build classpath
if "$DISTRIBUTION"; then
  # Core libraries
  for f in "$YCSB_HOME"/lib/*.jar; do
    [ -r "$f" ] && CLASSPATH="$CLASSPATH:$f"
  done

  # Database conf dir
  [ -r "$YCSB_HOME/$BINDING_DIR-binding/conf" ] && CLASSPATH="$CLASSPATH:$YCSB_HOME/$BINDING_DIR-binding/conf"

  # Database libraries
  for f in "$YCSB_HOME/$BINDING_DIR-binding/lib/*.jar"; do
    [ -r "$f" ] && CLASSPATH="$CLASSPATH:$f"
  done
else
  # Check for some basic libraries to see if the source has been built.
  if ! ls "$YCSB_HOME/core/target/"*.jar 1>/dev/null 2>&1 || \
     ! ls "$YCSB_HOME/$BINDING_DIR/target/"*.jar 1>/dev/null 2>&1; then
    # Call mvn to build source checkout.
    if [ "$BINDING_NAME" = "basic" ]; then
      MVN_PROJECT=core
    else
      MVN_PROJECT="$BINDING_DIR"-binding
    fi

    echo "[WARN] YCSB libraries not found. Attempting to build..." >&2
    if ! mvn -Psource-run -pl "site.ycsb:$MVN_PROJECT" -am package -DskipTests; then
      echo "[ERROR] Error trying to build project. Exiting." >&2
      exit 1
    fi
  fi

  # Core libraries
  for f in "$YCSB_HOME/core/target/"*.jar; do
    [ -r "$f" ] && CLASSPATH="$CLASSPATH:$f"
  done

  # Core dependency libraries
  for f in "$YCSB_HOME/core/target/dependency/"*.jar; do
    [ -r "$f" ] && CLASSPATH="$CLASSPATH:$f"
  done

  # Database conf (need to find because location is not consistent)
  CLASSPATH_CONF=$(find "$YCSB_HOME/$BINDING_DIR" -name "conf" | while IFS="" read -r file; do echo ":$file"; done)
  [ -n "$CLASSPATH_CONF" ] && CLASSPATH="$CLASSPATH$CLASSPATH_CONF"

  # Database libraries
  for f in "$YCSB_HOME/$BINDING_DIR/target/"*.jar; do
    [ -r "$f" ] && CLASSPATH="$CLASSPATH:$f"
  done

  # Database dependency libraries
  for f in "$YCSB_HOME/$BINDING_DIR/target/dependency/"*.jar; do
    [ -r "$f" ] && CLASSPATH="$CLASSPATH:$f"
  done
fi

# For Cygwin, switch paths to Windows format before running java
if "$CYGWIN"; then
  JAVA_HOME=$(cygpath --unix "$JAVA_HOME")
  CLASSPATH=$(cygpath --path --windows "$CLASSPATH")
fi

# Get the rest of the arguments
YCSB_ARGS="${@:3}"

# About to run YCSB
echo "$JAVA_HOME/bin/java $JAVA_OPTS -classpath \"$CLASSPATH\" $YCSB_CLASS $YCSB_COMMAND -db $BINDING_CLASS $YCSB_ARGS"

# Run YCSB
"$JAVA_HOME/bin/java" $JAVA_OPTS -classpath "$CLASSPATH" $YCSB_CLASS $YCSB_COMMAND -db "$BINDING_CLASS" "$YCSB_ARGS"
