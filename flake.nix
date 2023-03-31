{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        inherit (nixpkgs.lib) optional;
        pkgs = import nixpkgs {
          inherit system;
        };
      in
        with pkgs; rec {
          # packages = {};
          devShell = mkShell {
            name = "dev-shell";
            buildInputs = [pkgs.python3 pkgs.poetry pkgs.pylint pkgs.stdenv.cc.cc.lib pkgs.libstdcxx5];
            #resolution of libstdc++.so.6 error
            shellHook = ''
              export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
            '';
          };
        }
    );
}