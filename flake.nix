{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:bclaud/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        inherit (nixpkgs.lib) optional;
        pkgs = import nixpkgs {
          inherit system;
        };

        ci-tests = pkgs.writeScriptBin "ci-tests" "poetry install && MODE=tests poetry run python -m pytest";
      in
        with pkgs; rec {
          # packages = {};

          devShell = mkShell {
            name = "development-shell";
            buildInputs = [pkgs.python310 pkgs.poetry pkgs.pylint pkgs.stdenv.cc.cc.lib pkgs.libstdcxx5 ci-tests];
            #resolution of libstdc++.so.6 error
            shellHook = ''
              export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
            '';
          };
        }
    );
}