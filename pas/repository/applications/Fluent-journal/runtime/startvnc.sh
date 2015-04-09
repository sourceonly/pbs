#!/bin/bash
#PBS_JOBID=22.ee
#DIMENSION="3d"
#PRECISION="Double"
#MPI_TYPE="HPMPI"
#PAS_EXECUTABLE="fluent"
#echo ${MPI_TYPE}

unset 'OMP_NUM_THREADS'
#if [ "${MPI_TYPE}" == "HPMPI" ]
  # Set up environment for HP-MPI
#then
#  mpi_code='hp'
#elif [ "${MPI_TYPE}" == "IntelMPI" ]
#then
  # Set up environment for IntelMPI
#  mpi_code='intel'
#else
  # SMP run chosen
#  mpi_code="none"
#fi

if [ "${PRECISION}" == 'Double' ]
then
  PRECISION='dp'
else
  PRECISION=''
fi

echo DIMENSIONPRECISION=${DIMENSION}${PRECISION}

cmd=${PAS_EXECUTABLE}

NP=`cat ${PBS_NODEFILE} | wc -l`

if [ "${mpi_code}" != 'none' ] && [ "${PAS_VERSION}" == "14.5.0" ]
then
#  cmd="${cmd} ${DIMENSION}${PRECISION} -t${NP} -ssh -pib.openib -pcheck=0 -mpi=pcmpi -cnf=${PBS_NODEFILE}"
  cmd="${cmd} ${DIMENSION}${PRECISION} -t${NP} -ssh -pib -mpi=pcmpi -cnf=${PBS_NODEFILE}"
elif [ "${mpi_code}" != 'none' ] && [ "${PAS_VERSION}" == "12.1.0" ]
then
#  cmd="${cmd} ${DIMENSION}${PRECISION} -t${NP} -ssh -pib -pcheck=0 -mpi=hp -cnf=${PBS_NODEFILE}"
  cmd="${cmd} ${DIMENSION}${PRECISION} -t${NP} -ssh -pib -mpi=hp -cnf=${PBS_NODEFILE}"
fi

if [ "${PAS_CONNECT_ENABLED}" == "true" ]
then
  export TERM=xterm
  export PATH=/hpfs01/apps/vnc/TurboVNC/bin:$PATH
#  . /etc/X11/xorg.conf
  vncserver -noauth 2>${PBS_JOBID}.vnc
#  vncserver -noauth -noxstartup 2>${PBS_JOBID}.vnc
  #vncserver -auth 2>err
  VNCHOST=`hostname`
  vncid=`cat ${PBS_JOBID}.vnc|grep "desktop is $VNCHOST"|awk -F":" '{print $2}'`
  echo $vncid
  echo $VNCHOST":"$vncid >vncid
  export DISPLAY=$VNCHOST":"$vncid
#  rm -f ${PBS_JOBID}.vnc
else
  cmd="${cmd} -g"
fi

if [ "${JOURNAL}" ]
then
  cmd="${cmd} -i ${JOURNAL}"
fi

cmd="${cmd} >&${PBS_JOBNAME}.log"

echo "the cmd is ${cmd}"

${cmd}

#exit 0
